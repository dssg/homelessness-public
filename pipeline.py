import os, csv, subprocess
import pandas as pd
from matplotlib import pyplot as plt

run_weka = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_weka.sh')

class Pipeline:
    def __init__(self, data, file_path, feature_sets, targets, classifiers):
        self.data = data

        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weka', file_path)

        self.feature_sets = feature_sets # dict
        self.targets = targets # list
        self.classifiers = classifiers # dict

        self.models = {"{}_to_{}_by_{}".format(fsname, t, cname): (fsname, cname, fs, t, c) for fsname, fs in self.feature_sets.iteritems() for t in self.targets for cname, c in self.classifiers.iteritems()}

    def model(self):
        subprocess.Popen(['mkdir', '-p', self.file_path]).wait()
        procs = {}
        for model_name, (fs_name, cname, fs, t, c) in self.models.iteritems():
            # sort the dataframe by the target so that all models are classifying the same direction
            # (e.g. we don't want one model to classify as True and another to classify as False
            self.write_weka_csv(model_name, fs, t, self.data.sort(t, ascending=False))
            procs[model_name] = subprocess.Popen([run_weka, self.file_path, model_name, c])
        return [m.wait() for m in procs.values()]

    def write_weka_csv(self, model_name, feature_set, target, m):
        m[feature_set+[target]].dropna(subset=[target]).to_csv(os.path.join(self.file_path, model_name+'.csv'), na_rep='?', quoting=csv.QUOTE_NONNUMERIC, index=False)

    def plot_roc(self, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
        self.plot("'False Positive Rate'", "'True Positive Rate'", feature_sets, targets, classifiers, label_prefix)

    def plot_pr(self, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
        self.plot('Recall', 'Precision', feature_sets, targets, classifiers, label_prefix)

    def plot(self, x, y, feature_sets=None, targets=None, classifiers=None, label_prefix=''):
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
