"""The pipeline module.

Create a pipeline to build, run, analyze, and save and revisit models using Weka.  All results are saved into `weka/`,
so you can recreate the same pipeline, avoid re-running the model, but continue to use the same results. (See `README`
for more info`.)

NOTE: The pipeline takes feature_sets, targets, and classifiers, and computes *all possible combinations* of models for them.
So, if you give it 5 feature_sets, 5 targets, and 5 classifiers, you'll end up with 125 models.

"""
import os, csv, subprocess
import pandas as pd
from matplotlib import pyplot as plt

run_weka = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_weka.sh')

class Pipeline:
    def __init__(self, data, file_path, feature_sets, targets, classifiers):
        """Given a data frame, a file_path, (within `weka/`,) feature_sets, targets, and classifiers, construct a
        pipeline.  See the `models.ipynb` example notebook for an example.

        :param data: The dataframe to model.
        :type data: pandas.Dataframe
        :param file_path: The file path in which to put the results.
        :type file_path: str.
        :param feature_sets: The feature sets on which to model.
        :type feature_sets: dict, where keys are str and values are lists of str.
        :param targets: The targets sets on which to model.
        :type targets: list of str.
        :param classifiers: The classifiers to use for modeling.
        :type classifiers: dict, where keys are str and values are str.

        """
        self.data = data

        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weka', file_path)

        self.feature_sets = feature_sets # dict
        self.targets = targets # list
        self.classifiers = classifiers # dict

        self.models = {"{}_to_{}_by_{}".format(fsname, t, cname): (fsname, cname, fs, t, c) for fsname, fs in self.feature_sets.iteritems() for t in self.targets for cname, c in self.classifiers.iteritems()}

    def model(self):
        """Run the models, all in parallel.

        """
        subprocess.Popen(['mkdir', '-p', self.file_path]).wait()
        procs = {}
        for model_name, (fs_name, cname, fs, t, c) in self.models.iteritems():
            # sort the dataframe by the target so that all models are classifying the same direction
            # (e.g. we don't want one model to classify as True and another to classify as False
            self.write_weka_csv(model_name, fs, t, self.data.sort(t, ascending=False))
            procs[model_name] = subprocess.Popen([run_weka, self.file_path, model_name, c])
        return [m.wait() for m in procs.values()]

    def write_weka_csv(self, model_name, feature_set, target, m):
        """Write a CSV for Weka to use in file_path.


        """
        m[feature_set+[target]].dropna(subset=[target]).to_csv(os.path.join(self.file_path, model_name+'.csv'), na_rep='?', quoting=csv.QUOTE_NONNUMERIC, index=False)

    def plot_roc(self, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
        """Use output from :func:`model` to plot receiver-operator curves for all or a given subset of the models this
        pipeline embodies.  See `pipeline.ipynb` for an example.

        :param feature_sets: The feature sets to plot.
        :type feature_sets: list of str, the keys for the `feature_sets` for this pipeline.
        :param targets: The targets sets to plot.
        :type targets: list of str, matching the `targets` for this pipeline.
        :param classifiers: The classifiers to plot.
        :type feature_sets: list of str, the keys for the `classifiers` for this pipeline.

        """
        self.plot("'False Positive Rate'", "'True Positive Rate'", feature_sets, targets, classifiers, label_prefix)

    def plot_pr(self, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
        """Use output from :func:`model` to plot precision-recall curves for all or a given subset of the models this
        pipeline embodies.  See `pipeline.ipynb` for an example.

        :param feature_sets: The feature sets to plot.
        :type feature_sets: list of str, the keys for the `feature_sets` for this pipeline.
        :param targets: The targets sets to plot.
        :type targets: list of str, matching the `targets` for this pipeline.
        :param classifiers: The classifiers to plot.
        :type feature_sets: list of str, the keys for the `classifiers` for this pipeline.

        """
        self.plot('Recall', 'Precision', feature_sets, targets, classifiers, label_prefix)

    def plot(self, x, y, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
        """Helper method for :func:`plot_roc` and :func:`plot_rc`.

        """
        feature_sets = feature_sets or self.feature_sets
        targets = targets or self.targets
        classifiers = classifiers or self.classifiers

        for model_name, (fsname, cname, fs, t, c) in self.models.iteritems():
            if fsname in feature_sets and t in targets and cname in classifiers:
                thresholds = pd.read_csv(os.path.join(self.file_path, model_name+'_thresholds.csv'))
                plt.plot(thresholds[x], thresholds[y], label=label_prefix+model_name)
                plt.axis('image')
                plt.xlabel(x)
                plt.ylabel(y)
                plt.legend(loc=4)
