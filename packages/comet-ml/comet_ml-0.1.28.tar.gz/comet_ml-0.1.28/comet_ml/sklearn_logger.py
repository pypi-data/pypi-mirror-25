import sys
from importlib.machinery import PathFinder, ModuleSpec, SourceFileLoader
from comet_ml import config


def accuracy_score_logger(accuracy):
    def wrapper(*args, **kwargs):
        result = accuracy(*args, **kwargs)
        config.experiment.log_metric("accuracy",result)
        return result
    return wrapper

def fit_logger(real_fit):
    def wrapper(*args, **kwargs):
        print("in fit logger")
        return real_fit(*args, **kwargs)

    return wrapper


class Finder(PathFinder):

    def __init__(self, module_name, source, target, class_name = None):
        self.module_name = module_name
        self.source = source
        self.target = target
        self.class_name = class_name

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.module_name:
            spec = super().find_spec(fullname, path, target)
            loader = CustomLoader(fullname, spec.origin, self.source, self.target, self.class_name)
            return ModuleSpec(fullname, loader)

class CustomLoader(SourceFileLoader):

    def __init__(self,fullname, spec, source, target, class_name):
        super(CustomLoader, self).__init__(fullname,spec)
        self.source_func_name = source
        self.target_func = target
        self.class_name = class_name

    def exec_module(self, module):
        super().exec_module(module)

        if self.class_name is not None:
            class_pointer = getattr(module,self.class_name)
            source_func = getattr(class_pointer, self.source_func_name)
            source_func_logged = self.target_func(source_func)
            setattr(class_pointer,self.source_func_name,source_func_logged)
        else:
            source_func = getattr(module,self.source_func_name)
            source_func_logged = self.target_func(source_func)
            setattr(module, self.source_func_name, source_func_logged)

        return module

def patch():
    sys.meta_path.insert(0, Finder('sklearn.linear_model.stochastic_gradient', "fit", fit_logger,
                                   class_name="SGDClassifier"))
    #
    # sys.meta_path.insert(0, Finder('sklearn.metrics.classification',"accuracy_score", accuracy_score_logger))
    # sys.meta_path.insert(0, Finder('sklearn.pipeline',"fit", fit_logger, class_name="Pipeline"))
    #
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.weight_boosting', "fit", fit_logger,
    #                                class_name="AdaBoostClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.bagging', "fit", fit_logger, class_name="BaggingClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.naive_bayes', "fit", fit_logger, class_name="BernoulliNB"))
    # sys.meta_path.insert(0, Finder('sklearn.calibration', "fit", fit_logger, class_name="CalibratedClassifierCV"))
    # sys.meta_path.insert(0, Finder('sklearn.tree.tree', "fit", fit_logger, class_name="DecisionTreeClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.tree.tree', "fit", fit_logger, class_name="ExtraTreeClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.forest', "fit", fit_logger, class_name="ExtraTreesClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.naive_bayes', "fit", fit_logger, class_name="GaussianNB"))
    # sys.meta_path.insert(0, Finder('sklearn.gaussian_process.gpc', "fit", fit_logger,
    #                                class_name="GaussianProcessClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.gradient_boosting', "fit", fit_logger,
    #                                class_name="GradientBoostingClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.neighbors.classification', "fit", fit_logger,
    #                                class_name="KNeighborsClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.semi_supervised.label_propagation', "fit", fit_logger,
    #                                class_name="LabelPropagation"))
    # sys.meta_path.insert(0, Finder('sklearn.semi_supervised.label_propagation', "fit", fit_logger,
    #                                class_name="LabelSpreading"))
    # sys.meta_path.insert(0, Finder('sklearn.discriminant_analysis', "fit", fit_logger,
    #                                class_name="LinearDiscriminantAnalysis"))
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="LinearSVC"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.logistic', "fit", fit_logger,
    #                                class_name="LogisticRegression"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.logistic', "fit", fit_logger,
    #                                class_name="LogisticRegressionCV"))
    # sys.meta_path.insert(0, Finder('sklearn.neural_network.multilayer_perceptron', "fit", fit_logger,
    #                                class_name="MLPClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.naive_bayes', "fit", fit_logger, class_name="MultinomialNB"))
    # sys.meta_path.insert(0, Finder('sklearn.neighbors.nearest_centroid', "fit", fit_logger,
    #                                class_name="NearestCentroid"))
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="NuSVC"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.passive_aggressive', "fit", fit_logger,
    #                                class_name="PassiveAggressiveClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.perceptron', "fit", fit_logger, class_name="Perceptron"))
    # sys.meta_path.insert(0, Finder('sklearn.discriminant_analysis', "fit", fit_logger,
    #                                class_name="QuadraticDiscriminantAnalysis"))
    # sys.meta_path.insert(0, Finder('sklearn.neighbors.classification', "fit", fit_logger,
    #                                class_name="RadiusNeighborsClassifier"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.ensemble.forest', "fit", fit_logger, class_name="RandomForestClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.ridge', "fit", fit_logger, class_name="RidgeClassifier"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.ridge', "fit", fit_logger, class_name="RidgeClassifierCV"))
    #
    #
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="SVC"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.bayes', "fit", fit_logger, class_name="ARDRegression"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.weight_boosting', "fit", fit_logger,
    #                                class_name="AdaBoostRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.bagging', "fit", fit_logger, class_name="BaggingRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.bayes', "fit", fit_logger, class_name="BayesianRidge"))
    # sys.meta_path.insert(0, Finder('sklearn.cross_decomposition.cca_', "fit", fit_logger, class_name="CCA"))
    # sys.meta_path.insert(0, Finder('sklearn.tree.tree', "fit", fit_logger, class_name="DecisionTreeRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="ElasticNet"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="ElasticNetCV"))
    # sys.meta_path.insert(0, Finder('sklearn.tree.tree', "fit", fit_logger, class_name="ExtraTreeRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.forest', "fit", fit_logger, class_name="ExtraTreesRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.gaussian_process.gaussian_process', "fit", fit_logger,
    #                                class_name="GaussianProcess"))
    # sys.meta_path.insert(0, Finder('sklearn.gaussian_process.gpr', "fit", fit_logger,
    #                                class_name="GaussianProcessRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.ensemble.gradient_boosting', "fit", fit_logger,
    #                                class_name="GradientBoostingRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.huber', "fit", fit_logger, class_name="HuberRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.neighbors.regression', "fit", fit_logger,
    #                                class_name="KNeighborsRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.kernel_ridge', "fit", fit_logger, class_name="KernelRidge"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.least_angle', "fit", fit_logger, class_name="Lars"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.least_angle', "fit", fit_logger, class_name="LarsCV"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger, class_name="Lasso"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger, class_name="LassoCV"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.least_angle', "fit", fit_logger, class_name="LassoLars"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.least_angle', "fit", fit_logger, class_name="LassoLarsCV"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.least_angle', "fit", fit_logger, class_name="LassoLarsIC"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.base', "fit", fit_logger, class_name="LinearRegression"))
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="LinearSVR"))
    # sys.meta_path.insert(0, Finder('sklearn.neural_network.multilayer_perceptron', "fit", fit_logger,
    #                                class_name="MLPRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="MultiTaskElasticNet"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="MultiTaskElasticNetCV"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="MultiTaskLasso"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.coordinate_descent', "fit", fit_logger,
    #                                class_name="MultiTaskLassoCV"))
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="NuSVR"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.omp', "fit", fit_logger,
    #                                class_name="OrthogonalMatchingPursuit"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.omp', "fit", fit_logger,
    #                                class_name="OrthogonalMatchingPursuitCV"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.cross_decomposition.pls_', "fit", fit_logger, class_name="PLSCanonical"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.cross_decomposition.pls_', "fit", fit_logger, class_name="PLSRegression"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.passive_aggressive', "fit", fit_logger,
    #                                class_name="PassiveAggressiveRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.ransac', "fit", fit_logger, class_name="RANSACRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.neighbors.regression', "fit", fit_logger,
    #                                class_name="RadiusNeighborsRegressor"))
    # sys.meta_path.insert(0,
    #                      Finder('sklearn.ensemble.forest', "fit", fit_logger, class_name="RandomForestRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.ridge', "fit", fit_logger, class_name="Ridge"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.ridge', "fit", fit_logger, class_name="RidgeCV"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.stochastic_gradient', "fit", fit_logger,
    #                                class_name="SGDRegressor"))
    # sys.meta_path.insert(0, Finder('sklearn.svm.classes', "fit", fit_logger, class_name="SVR"))
    # sys.meta_path.insert(0, Finder('sklearn.linear_model.theil_sen', "fit", fit_logger,
    #                                class_name="TheilSenRegressor"))

if "sklearn" in sys.modules:
    raise SyntaxError("Please import comet before importing any sklearn modules")

patch()

#https://blog.sqreen.io/dynamic-instrumentation-agent-for-python/

