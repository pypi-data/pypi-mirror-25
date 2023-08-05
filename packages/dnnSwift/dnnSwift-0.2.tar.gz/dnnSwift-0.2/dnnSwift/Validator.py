import numpy as np
import pickle


class Validator(object):
    """
    This class validates the output of a tensorflow network with ground-truth
    labels. If the network output isn't normalized, a softmax normalization
    can be performed prior to further processing.
    """

    def __repr__(self):
        """
        A shortcut function to print the top-1 accuracy
        :return:
        """
        return "Accuracy: " + str(self._top_n_acc[1])

    def __str__(self):
        """
        A shortcut function to print the top-1 accuracy
        :return:
        """
        return "Accuracy: " + str(self._top_n_acc[1])

    def __init__(
            self, network_output, labels, image_groups, perform_softmax=True):
        """
        This class validates the output of a tensorflow network with
        ground-truth labels. If the network output isn't normalized, a softmax
        normalization is performed prior to processing.

        The labels must be one-hot vectors, e.g.
        labels = [[0, 0, 1],
                  [0, 1, 0],
                  [0, 0, 1],
                  [1, 0, 0]]

        :param network_output: Numpy array. Output of a tensorflow network.
            Should have the shape (num_samples, num_labels)
        :param labels: Numpy array. The ground truth of the network output
            being validated. Should have the shape (num_samples, num_labels).
        :param image_groups: A dictionary indicating which one-hot vector
            belongs to which category, e.g.
            {"Category_1": 0, "Category_2": 1, ...}
        :param perform_softmax: A boolean value indicating if the network
            output should be normalized
        """

        if len(image_groups) != labels.shape[1]:
            raise ValueError(
                "The label vectors should have the same dimension (%s) as the "
                "number of image groups (%s)" %
                (labels.shape[1], len(image_groups)))

        if network_output.shape != labels.shape:
            raise ValueError(
                "'network_output' and 'labels' must have the same shape")

        if set(np.unique(labels)) != {1, 0}:
            raise ValueError(
                "'labels' must be a series of one-hot vectors")

        if set(np.sum(labels, axis=1)) != {1}:
            raise ValueError(
                "'labels' must be a series of one-hot vectors")

        self._network_output = network_output.astype(np.float128)
        self._labels = labels
        self._image_groups = image_groups

        # Perform softmax if required
        # The softmax function is invariant against additive shifts in the
        # input vectors, i.e.
        #     exp(x) / sum(exp(x)) == exp(x + C) / sum(exp(x + C))
        # C is set to be the maximum value of each probability vector. That
        # way, exp(x + X) is guaranteed to not cause any numerical overflows,
        # e.g.
        #   - np.exp((1e5, 5e4, 1e3)) == (inf, inf, 1.97e+434) but
        #     np.exp((0, -5e4, -9.9e4)) == (1.0, 0.0, 0.0)
        if perform_softmax:
            max_out = np.max(self._network_output, axis=1, keepdims=True)
            self._network_output = np.exp(self._network_output - max_out)
            self._network_output /= np.sum(
                self._network_output, 1, keepdims=True)

        # Determine all metrics
        # Calculate all top-n-accuracies for n from 1 to num_categories
        self._top_n_acc = {}
        for i in range(1, self._network_output.shape[1]+1):
            self._top_n_acc[i] = self.calc_top_n_accuracy(n=i)

        # Precision-Recall
        pr = self.calc_precision_recall()
        self._precision = pr["precision"]
        self._recall = pr["recall"]
        self._counts = pr["counts"]
        self._thresholds = pr["thresholds"]

        # Get the total number of validation data for each category
        cat_invert = {v: k for k, v in self._image_groups.items()}
        self._img_freq = {
            cat_invert[k]: v for k, v in zip(*np.unique(np.argmax(
                self._labels, axis=1), return_counts=True))}

        # Calculate the loss
        loss = self.calc_loss()
        self._ce_loss = loss["cross_entropy"]
        self._rmse_loss = loss["RMSE"]

    def get_top_n_acc(self):
        return self._top_n_acc

    def get_top_1_acc(self):
        return self._top_n_acc[1]

    def get_ce_loss(self):
        return self._ce_loss

    def get_rmse_loss(self):
        return self._rmse_loss

    @DeprecationWarning
    def get_cat_collapse_acc(self):
        return None

    def get_precision(self):
        return self._precision

    def get_recall(self):
        return self._recall

    def get_counts(self):
        return self._counts

    def get_thresholds(self):
        return self._thresholds

    def save_results(self, filename):
        with open(filename, "wb") as f:
            val_dict = {"precision": self._precision, "recall": self._recall,
                        "counts": self._counts, "top_n_acc": self._top_n_acc,
                        "top_1_acc": self._top_n_acc[1],
                        "data_counts": self._img_freq,
                        "cross_entropy_loss": self._ce_loss,
                        "rmse_loss": self._rmse_loss}
            pickle.dump(val_dict, f, pickle.HIGHEST_PROTOCOL)

    def calc_top_n_accuracy(self, n):
        """
        Calculate the top-n accuracy, i.e. the probability that the correct
        label is in the top 'n' predicted classes.
        :param n: An integer >= 1, e.g. n == X -> the correct label must be
            in the the top X most likely predictions.
        :return:
        """

        if n < 1:
            raise ValueError("'n' must be >= 1")

        # Calculate the rank of every entry (ascending order)
        # A single argsort returns the order and the second argsort returns the
        # rank of each entry
        argrank = np.argsort(a=np.argsort(
            a=self._network_output, axis=1), axis=1)

        # Invert the sorting (so that it is in descending order
        argrank = np.max(argrank, axis=1, keepdims=True) - argrank

        # Mark all predicted labels that are in the top 'n' categories
        argrank = argrank <= (n-1)

        # Transform the labels into a boolean array
        labels = self._labels == np.max(self._labels, axis=1, keepdims=True)

        # The accuracy is the logical AND for each row, i.e. the product of
        # the two boolean vectors
        return np.mean(np.sum(argrank * labels, axis=1))

    def calc_precision_recall(self):
        """
        Determines precision-recall statistics based on the probability
        threshold used to determine the categories.
        :return:
        """

        network_output_binary = np.argmax(self._network_output, 1)
        network_output_max_prob = np.max(self._network_output, 1)
        labels_binary = np.argmax(self._labels, 1)

        # Define thresholds. The minimum is the 'relative majority',
        # so 1/n_categories and the maximum is 1
        thresholds = np.linspace(1.0 / self._labels.shape[1], 1, 20)

        all_precisions = {}
        all_recalls = {}
        all_counts = {}
        for cat in self._image_groups.keys():
            value = self._image_groups[cat]
            precision = []
            recall = []
            counts = []
            for t in thresholds:
                nob_copy = np.copy(network_output_binary)
                nob_copy[network_output_max_prob < t] = -1
                if sum(nob_copy == value) == 0:
                    precision.append(float("nan"))
                else:
                    precision.append(
                        1.0 *
                        sum((labels_binary == value) *
                            (nob_copy == value)) /
                        sum(nob_copy == value))

                if sum(labels_binary == value) == 0:
                    recall.append(float("nan"))
                else:
                    recall.append(
                        1.0 *
                        sum((labels_binary == value) *
                            (nob_copy == value)) /
                        sum(labels_binary == value))

                counts.append(sum(nob_copy == value))

            all_precisions[cat] = precision
            all_recalls[cat] = recall
            all_counts[cat] = counts

        return {
            "precision": all_precisions, "recall": all_recalls,
            "counts": all_counts, "thresholds": thresholds}

    def calc_loss(self):
        """
        Calculates the cross entropy and RMSE loss
        :return:
        """

        ce_loss = np.mean(-1 * np.sum(np.log2(
            self._network_output) * self._labels, axis=1))
        rmse_loss = np.sqrt(np.mean(np.square(
            self._network_output - self._labels)[0:3, ...]))
        return {"cross_entropy": ce_loss, "RMSE": rmse_loss}

