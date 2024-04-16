# BlueCast

[![codecov](https://codecov.io/gh/ThomasMeissnerDS/BlueCast/branch/main/graph/badge.svg?token=XRIS04O097)](https://codecov.io/gh/ThomasMeissnerDS/BlueCast)
[![Codecov workflow](https://github.com/ThomasMeissnerDS/BlueCast/actions/workflows/workflow.yaml/badge.svg)](https://github.com/ThomasMeissnerDS/BlueCast/actions/workflows/workflow.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)
[![Documentation Status](https://readthedocs.org/projects/bluecast/badge/?version=latest)](https://bluecast.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/bluecast.svg)](https://pypi.python.org/pypi/bluecast/)
[![Optuna](https://img.shields.io/badge/Optuna-integrated-blue)](https://optuna.org)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A lightweight and fast auto-ml library.
BlueCast focuses on a few model architectures (on default Xgboost
only) and a few preprocessing options (only what is
needed for Xgboost). This allows for a much faster development
cycle and a much more stable codebase while also having as few dependencies
as possible for the library. Despite being lightweight in its core BlueCast
offers high customization options for advanced users. Find
the full documentation [here](https://bluecast.readthedocs.io/en/latest/).

Here you can see our test coverage in more detail:

[![Codecov sunburst](https://codecov.io/gh/ThomasMeissnerDS/BlueCast/graphs/sunburst.svg?token=XRIS04O097)](https://codecov.io/gh/ThomasMeissnerDS/BlueCast/graphs/sunburst.svg?token=XRIS04O097)

<!-- toc -->

* [Installation](#installation)
  * [Installation for end users](#installation-for-end-users)
  * [Installation for developers](#installation-for-developers)
* [General usage](#general-usage)
  * [Basic usage](#basic-usage)
  * [Advanced usage](#advanced-usage)
    * [Explanatory analysis](#explanatory-analysis)
    * [Leakage detection](#leakage-detection)
    * [Enable cross-validation](#enable-cross-validation)
    * [Enable even more overfitting-robust cross-validation](#enable-even-more-overfitting-robust-cross-validation)
    * [Gaining extra performance](#gaining-extra-performance)
    * [Use multi-model blended pipeline](#use-multi-model-blended-pipeline)
    * [Categorical encoding](#categorical-encoding)
    * [Custom training configuration](#custom-training-configuration)
    * [Custom preprocessing](#custom-preprocessing)
    * [Custom feature selection](#custom-feature-selection)
    * [Custom ML model](#custom-ml-model)
    * [Using the inbuilt ExperientTracker](#using-the-inbuilt-experienttracker)
    * [Gain insights across experiments](#gain-insights-across-experiments)
    * [Use Mlflow via custom ExperientTracker API](#use-mlflow-via-custom-experienttracker-api)
    * [Custom data drift checker](#custom-data-drift-checker)
  * [Model explainability](#model-explainability)
    * [Hyperparameter tuning](#hyperparameter-tuning)
    * [Model performance](#model-performance)
    * [SHAP values](#shap-values)
  * [Conformal prediction](#conformal-prediction)
  * [Plotting decision trees](#plotting-decision-trees)
    * [Accessing the trained models](#accessing-the-trained-models)
      * [BlueCast classes](#bluecast-classes)
      * [BlueCastCV classes](#bluecastcv-classes)
* [Convenience features](#convenience-features)
* [Code quality](#code-quality)
* [Documentation](#documentation)
* [Kaggle competition results and example notebooks](#kaggle-competition-results-and-example-notebooks)
* [How to contribute](#how-to-contribute)
* [Meta](#meta)

<!-- tocstop -->

## Installation

### Installation for end users

From PyPI:

```sh
pip install bluecast
```

Using a fresh environment with Python 3.9 or higher is recommended. We consciously
do not support Python 3.8 or lower to prevent the usage of outdated Python versions
and issues connected to it.

### Installation for developers

* Clone the repository:
* Create a new conda environment with Python 3.9 or higher
* run `pip install poetry` to install poetry as dependency manager
* run `poetry install` to install all dependencies

## General usage

### Basic usage

The module blueprints contains the main functionality of the library. The main
entry point is the `Blueprint` class. It already includes needed preprocessing
(including some convenience functionality like feature type detection)
and model hyperparameter tuning.

```sh
from bluecast.blueprints.cast import BlueCast

automl = BlueCast(
        class_problem="binary",
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)

# from version 0.95 also predict_proba is directly available (also for BlueCastCV)
y_probs = automl.predict_proba(df_val)
```

BlueCast has simple utilities to save and load your pipeline:

```sh
from bluecast.general_utils.general_utils import save_to_production, load_for_production

# save pipeline including tracker
save_to_production(automl, "/kaggle/working/", "bluecast_cv_pipeline")

# in production or for further experiments this can be loaded again
automl = load_for_production("/kaggle/working/", "bluecast_cv_pipeline")
```

Since version 0.80 BlueCast offers regression as well:

```sh
from bluecast.blueprints.cast_regression import BlueCastRegression

automl = BlueCast(
        class_problem="regression",
    )

automl.fit(df_train, target_col="target")
y_hat = automl.predict(df_val)
```

### Advanced usage

#### Explanatory analysis

BlueCast offers a simple way to get a first overview of the data:

```sh
from bluecast.eda.analyse import (
    bi_variate_plots,
    univariate_plots,
    plot_count_pairs,
    correlation_heatmap,
    correlation_to_target,
    plot_pca,
    plot_pca_cumulative_variance,
    plot_theil_u_heatmap,
    plot_tsne,
    check_unique_values,
    plot_null_percentage,
    mutual_info_to_target.
    plot_pie_chart,
)

from bluecast.preprocessing.feature_types import FeatureTypeDetector

# Here we automatically detect the numeric columns
feat_type_detector = FeatureTypeDetector()
train_data = feat_type_detector.fit_transform_feature_types(train_data)

# detect columns with a very high share of unique values
many_unique_cols = check_unique_values(train_data, feat_type_detector.cat_columns)
```

```sh
# plot the percentage of Nulls for all features
plot_pie_chart(
        synthetic_train_test_data[0],
        "categorical_feature_1",
    )
```

![QQplot example](docs/source/pie_chart.png)

```sh
# plot the percentage of Nulls for all features
plot_null_percentage(
    train_data.loc[:, feat_type_detector.num_columns],
    )
```

![QQplot example](docs/source/plot_nulls.png)

```sh
# show univariate plots
univariate_plots(
        train_data.loc[:, feat_type_detector.num_columns],  # here the target column EC1 is already included
    )
```

![QQplot example](docs/source/univariate_plots.png)

```sh
# show bi-variate plots
bi_variate_plots(
    train_data.loc[:, feat_type_detector.num_columns],
      "EC1"
      )
```

![QQplot example](docs/source/bivariate_plots.png)

```sh
# show bi-variate plots
plot_count_pairs(
    train,
    test,
    cat_cols=train_data.loc[:, feat_type_detector.cat_columns],
      )
```

![QQplot example](docs/source/pair_countplot.png)

```sh
# show correlation to target
correlation_to_target(train_data.loc[:, feat_type_detector.num_columns])
```

![QQplot example](docs/source/correlation_to_target.png)

```sh
# show correlation heatmap
correlation_heatmap(train_data.loc[:, feat_type_detector.num_columns])
```

![QQplot example](docs/source/correlation_heatmap.png)

```sh
# show a heatmap of assocations between categorical variables
theil_matrix = plot_theil_u_heatmap(train_data, feat_type_detector.cat_columns)
```

![QQplot example](docs/source/theil_u_matrix.png)

```sh
# show mutual information of categorical features to target
# features are expected to be numerical format
# class problem can be any of "binary", "multiclass" or "regression"
extra_params = {"random_state": 30}
mutual_info_to_target(train_data.loc[:, feat_type_detector.num_columns], "EC1", class_problem="binary", **extra_params)
```

![QQplot example](docs/source/mutual_information.png)

```sh
## show feature space after principal component analysis
plot_pca(
    train_data.loc[:, feat_type_detector.num_columns],
    "target"
    )
```

![QQplot example](docs/source/plot_pca.png)

```sh
## show how many components are needed to explain certain variance
plot_pca_cumulative_variance(
    train_data.loc[:, feat_type_detector.num_columns],
    "target"
    )
```

![QQplot example](docs/source/plot_cumulative_pca_variance.png)

```sh
# show feature space after t-SNE
plot_tsne(
    train_data.loc[:, feat_type_detector.num_columns],
    "target",
    perplexity=30,
    random_state=0
    )
```

![QQplot example](docs/source/t_sne_plot.png)

#### Leakage detection

With big data and complex pipelines data leakage can easily sneak in.
To detect leakage BlueCast offers two functions:

```sh
from bluecast.eda.data_leakage_checks import (
    detect_categorical_leakage,
    detect_leakage_via_correlation,
)


# Detect leakage of numeric columns based on correlation
result = detect_leakage_via_correlation(
        train_data.loc[:, feat_type_detector.num_columns], "target", threshold=0.9
    )

# Detect leakage of categorical columns based on Theil's U
result = detect_categorical_leakage(
        train_data.loc[:, feat_type_detector.cat_columns], "target", threshold=0.9
    )
```

#### Enable cross-validation

While the default behaviour of BlueCast is to use a simple
train-test-split, cross-validation can be enabled easily:

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.config.training_config import TrainingConfig


# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hypertuning_cv_folds = 5 # default is 1

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

This will use Xgboost's inbuilt cross validation routine which allows BlueCast
to execute early pruning on not promising hyperparameter sets. This way BlueCast
can test many more hyperparameters than usual cross validation.

#### Enable even more overfitting-robust cross-validation

There might be situations where a preprocessing step has a high risk of overfitting
and  needs even more careful evaluation (i.e. oversampling techniques). For such
scenarios BlueCast offers a solution as well.

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.config.training_config import TrainingConfig


# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hypertuning_cv_folds = 5 # default is 1
train_config.precise_cv_tuning = True # this enables the better routine

# this only makes sense if we have an overfitting risky step
custom_preprocessor = MyCustomPreprocessing() # see section Custom Preprocessing for details

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
        custom_in_fold_preprocessor=custom_preprocessor # this happens during each fold
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

The custom in fold preprocessing takes place within the cross validation and
executes the step on each fold. The evaluation metric is special here:
Instead of calculating matthews correlation coefficient reversed only,
it applied increasingly random noise to the eval dataset to find an even
more robust hyperparameter set.

This is much more robust, but does not offer
early pruning and is much slower. BlueCastCV supports this as well.

Please note that this is an experimental feature.

#### Gaining extra performance

By default BlueCast uses Optuna's Bayesian hyperparameter optimization,
however Bayesian methods give an estimate and do not necessarly find
the ideal spot, thus BlueCast has an optional GridSearch setting
that allows BlueCast to refine some of the parameters Optuna has found.
This can be enabled by setting `enable_grid_search_fine_tuning` to True.
This fine-tuning step uses a different random seed than the autotuning
routine (seed from the settings + 1000).

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.config.training_config import TrainingConfig


# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hypertuning_cv_folds = 5 # default is 1
train_config.enable_grid_search_fine_tuning = True # default is False
train_config.gridsearch_tuning_max_runtime_secs = 3600 # max runtime in secs
train_config.gridsearch_nb_parameters_per_grid = 5 # increasing this means X^3 trials atm

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

This comes with a tradeoff of longer runtime. This behaviour can be further
controlled with two parameters:

* `gridsearch_nb_parameters_per_grid`: Decides how
  many steps the grid shall have per parameter
* `gridsearch_tuning_max_runtime_secs`: Sets the maximum time in seconds
  the tuning shall run. This will finish the latest trial nd will exceed
  this limit though.

#### Use multi-model blended pipeline

By default, BlueCast trains a single model. However, it is possible to
train multiple models with one call for extra robustness. `BlueCastCV`
has a `fit` and a `fit_eval` method. The `fit_eval` method trains the
models, but also provides out-of-fold validation. Also `BlueCastCV`
allows to pass custom configurations.

```sh
from bluecast.blueprints.cast_cv import BlueCastCV
from bluecast.config.training_config import TrainingConfig, XgboostTuneParamsConfig

# Pass the custom configs to the BlueCast class
automl = BlueCastCV(
        class_problem="binary",
        #conf_training=train_config,
        #conf_xgboost=xgboost_param_config,
        #custom_preprocessor=custom_preprocessor, # this takes place right after test_train_split
        #custom_last_mile_computation=custom_last_mile_computation, # last step before model training/prediction
        #custom_feature_selector=custom_feature_selector,
    )

# this class has a train method:
# automl.fit(df_train, target_col="target")

automl.fit_eval(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

Also here a variant for regression is available:

```sh
from bluecast.blueprints.cast_cv_regression import BlueCastCVRegression
from bluecast.config.training_config import TrainingConfig, XgboostTuneParamsConfig

# Pass the custom configs to the BlueCast class
automl = BlueCastCVRegression(
        class_problem="regression",
        #conf_training=train_config,
        #conf_xgboost=xgboost_param_config,
        #custom_preprocessor=custom_preprocessor, # this takes place right after test_train_split
        #custom_last_mile_computation=custom_last_mile_computation, # last step before model training/prediction
        #custom_feature_selector=custom_feature_selector,
    )

# this class has a train method:
# automl.fit(df_train, target_col="target")

automl.fit_eval(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

#### Categorical encoding

By default, BlueCast uses onehot and target encoding. An orchestrator measures the
columns' cardinality and routes each categorical column to onehot or target encoding.
Onehot encoding is applied when the cardinality is less or equal
`cardinality_threshold_for_onehot_encoding` from the training config (5 by default).

This behaviour can be changed in the TrainingConfig by setting `cat_encoding_via_ml_algorithm`
to True. This will change the expectations of `custom_last_mile_computation` though.
If `cat_encoding_via_ml_algorithm` is set to False, `custom_last_mile_computation`
will receive numerical features only as target encoding will apply before. If `cat_encoding_via_ml_algorithm`
is True (default setting) `custom_last_mile_computation` will receive categorical
features as well, because Xgboost's or a custom model's inbuilt categorical encoding
will be used.

#### Custom training configuration

Despite e2eml, BlueCast allows easy customization. Users can adjust the
configuration and just pass it to the `BlueCast` class. Here is an example:

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.config.training_config import TrainingConfig, XgboostTuneParamsConfig

# Create a custom tuning config and adjust hyperparameter search space
xgboost_param_config = XgboostTuneParamsConfig()
xgboost_param_config.steps_max = 100
xgboost_param_config.max_leaves_max = 16
# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hyperparameter_tuning_rounds = 10
train_config.autotune_model = False # we want to run just normal training, no hyperparameter tuning
# We could even just overwrite the final Xgboost params using the XgboostFinalParamConfig class

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
        conf_xgboost=xgboost_param_config,
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

#### Custom preprocessing

The `BlueCast` class also allows for custom preprocessing. This is done by
an abstract class that can be inherited and passed into the `BlueCast` class.
BlueCast provides two entry points to inject custom preprocessing. The
attribute `custom_preprocessor` is called right after the train_test_split.
The attribute `custom_last_mile_computation` will be called before the model
training or prediction starts (when only numerical features are present anymore)
and allows users to execute last computations (i.e. sub sampling or final calculations).

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.preprocessing.custom import CustomPreprocessing

# Create a custom tuning config and adjust hyperparameter search space
xgboost_param_config = XgboostTuneParamsConfig()
xgboost_param_config.steps_max = 100
xgboost_param_config.max_leaves_max = 16
# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hyperparameter_tuning_rounds = 10
train_config.autotune_model = False # we want to run just normal training, no hyperparameter tuning
# We could even just overwrite the final Xgboost params using the XgboostFinalParamConfig class

class MyCustomPreprocessing(CustomPreprocessing):
    def __init__(self):
        self.trained_patterns = {}

    def fit_transform(
        self, df: pd.DataFrame, target: pd.Series
    ) -> Tuple[pd.DataFrame, pd.Series]:
        num_columns = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'], axis=1).columns
        cat_df = df[['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ']].copy()

        zscores = Zscores()
        zscores.fit_all(df, ['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'])
        df = zscores.transform_all(df, ['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'])
        self.trained_patterns["zscores"] = zscores

        imp_mean = SimpleImputer(missing_values=np.nan, strategy='median')
        num_columns = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'], axis=1).columns
        imp_mean.fit(df.loc[:, num_columns])
        df = imp_mean.transform(df.loc[:, num_columns])
        self.trained_patterns["imputation"] = imp_mean

        df = pd.DataFrame(df, columns=num_columns).merge(cat_df, left_index=True, right_index=True, how="left")

        df = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha'], axis=1)

        return df, target

    def transform(
        self,
        df: pd.DataFrame,
        target: Optional[pd.Series] = None,
        predicton_mode: bool = False,
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        num_columns = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'], axis=1).columns
        cat_df = df[['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ']].copy()

        df = self.trained_patterns["zscores"].transform_all(df, ['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'])

        imp_mean = self.trained_patterns["imputation"]
        num_columns = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha', 'EJ'], axis=1).columns
        df.loc[:, num_columns] = df.loc[:, num_columns].replace([np.inf, -np.inf], np.nan)
        df = imp_mean.transform(df.loc[:, num_columns])

        df = pd.DataFrame(df, columns=num_columns).merge(cat_df, left_index=True, right_index=True, how="left")

        df = df.drop(['Beta', 'Gamma', 'Delta', 'Alpha'], axis=1)

        return df, target

# add custom last mile computation
class MyCustomLastMilePreprocessing(CustomPreprocessing):
    def custom_function(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df / 2
        df["custom_col"] = 5
        return df

    # Please note: The base class enforces that the fit_transform method is implemented
    def fit_transform(
        self, df: pd.DataFrame, target: pd.Series
    ) -> Tuple[pd.DataFrame, pd.Series]:
        df = self.custom_function(df)
        df = df.head(1000)
        target = target.head(1000)
        return df, target

    # Please note: The base class enforces that the fit_transform method is implemented
    def transform(
        self,
        df: pd.DataFrame,
        target: Optional[pd.Series] = None,
        predicton_mode: bool = False,
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        df = self.custom_function(df)
        if not predicton_mode and isinstance(target, pd.Series):
            df = df.head(100)
            target = target.head(100)
        return df, targe

custom_last_mile_computation = MyCustomLastMilePreprocessing()
custom_preprocessor = MyCustomPreprocessing()

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
        conf_xgboost=xgboost_param_config,
        custom_preprocessor=custom_preprocessor, # this takes place right after test_train_split
        custom_last_mile_computation=custom_last_mile_computation, # last step before model training/prediction
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

#### Custom feature selection

BlueCast offers automated feature selection. On default the feature
selection is disabled, but BlueCast raises a warning to inform the
user about this option. The behaviour can be controlled via the
`TrainingConfig`.

```sh
from bluecast.blueprints.cast import BlueCast
from bluecast.preprocessing.custom import CustomPreprocessing
from bluecast.config.training_config import TrainingConfig

# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.hyperparameter_tuning_rounds = 10
train_config.autotune_model = False # we want to run just normal training, no hyperparameter tuning
train_config.enable_feature_selection = True

# Pass the custom configs to the BlueCast class
automl = BlueCast(
        class_problem="binary",
        conf_training=train_config,
    )

automl.fit(df_train, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

Also this step can be customized. The following example shows how to:

```sh
from bluecast.config.training_config import TrainingConfig
from bluecast.preprocessing.custom import CustomPreprocessing
from sklearn.feature_selection import RFECV
from sklearn.metrics import make_scorer, matthews_corrcoef
from sklearn.model_selection import StratifiedKFold
from typing import Optional, Tuple


# Create a custom training config and adjust general training parameters
train_config = TrainingConfig()
train_config.enable_feature_selection = True

# add custom feature selection
class RFECVSelector(CustomPreprocessing):
    def __init__(self, random_state: int = 0):
        super().__init__()
        self.selected_features = None
        self.random_state = random_state
        self.selection_strategy: RFECV = RFECV(
            estimator=xgb.XGBClassifier(),
            step=1,
            cv=StratifiedKFold(5, random_state=random_state, shuffle=True),
            min_features_to_select=1,
            scoring=make_scorer(matthews_corrcoef),
            n_jobs=2,
        )

    def fit_transform(self, df: pd.DataFrame, target: pd.Series) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        self.selection_strategy.fit(df, target)
        self.selected_features = self.selection_strategy.support_
        df = df.loc[:, self.selected_features]
        return df, target

    def transform(self,
                  df: pd.DataFrame,
                  target: Optional[pd.Series] = None,
                  predicton_mode: bool = False) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        df = df.loc[:, self.selected_features]
        return df, target

custom_feature_selector = RFECVSelector()

# Create an instance of the BlueCast class with the custom model
bluecast = BlueCast(
    class_problem="binary",
    conf_feature_selection=custom_feat_sel,
    conf_training=train_config,
    custom_feature_selector=custom_feature_selector,

# Create some sample data for testing
x_train = pd.DataFrame(
    {"feature1": [i for i in range(10)], "feature2": [i for i in range(10)]}
)
y_train = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
x_test = pd.DataFrame(
    {"feature1": [i for i in range(10)], "feature2": [i for i in range(10)]}

x_train["target"] = y_trai
# Fit the BlueCast model using the custom model
bluecast.fit(x_train, "target"
# Predict on the test data using the custom model
predicted_probas, predicted_classes = bluecast.predict(x_test)
```

#### Custom ML model

For some users it might just be convenient to use the BlueCast class to
enjoy convenience features (details see below), but use a custom ML model.
This is possible by passing a custom model to the BlueCast class. The needed properties
are defined via the BaseClassMlModel class. Here is an example:

```sh
from bluecast.ml_modelling.base_classes import (
    BaseClassMlModel,
    PredictedClasses,  # just for linting checks
    PredictedProbas,  # just for linting checks
)

class CustomModel(BaseClassMlModel):
    def __init__(self):
        self.model = None

    def autotune(
        self,
        x_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ):

        eval_dataset = Pool(x_test, y_test, cat_features=["DMAR", "LD_INDL", "RF_CESAR", "SEX"])

        alpha = 0.05
        quantile_levels = [alpha, 1 - alpha]
        quantile_str = str(quantile_levels).replace('[','').replace(']','')

        def objective(trial):
            # this part is taken from: https://www.kaggle.com/code/syerramilli/catboost-multi-quantile-regression
            param = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 2000, log=True),
                "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 5, 100),
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
                'depth': trial.suggest_int('depth', 2, 10, log=True),
                "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-3, 1e6),
                'colsample_bylevel': trial.suggest_float("colsample_bylevel", 0.1, 1),
                'subsample': trial.suggest_float("subsample", 0.3, 1)
            }
            model = CatBoostRegressor(
                loss_function=f'MultiQuantile:alpha={quantile_str}',
                thread_count= 4,
                cat_features=["DMAR", "LD_INDL", "RF_CESAR", "SEX"],
                bootstrap_type =  "Bernoulli",
                sampling_frequency= 'PerTree',
                **param
            )

            # train model
            model.fit(x_train, y_train, verbose=0)

            # get predictions
            preds = model.predict(x_test)

            # get perfomance metrics
            MWIS, coverage = MWIS_metric.score(
                y_test, preds[:, 0], preds[:, 1], alpha=0.1
            )

            if coverage < 0.9:
                raise optuna.exceptions.TrialPruned()

            return MWIS

        sampler = optuna.samplers.TPESampler(
                multivariate=True, seed=1000
            )
        study = optuna.create_study(
            direction="minimize", sampler=sampler, study_name=f"catboost"
        )
        study.optimize(
            objective,
            n_trials=500,
            timeout=60 * 60 * 2,
            gc_after_trial=True,
            show_progress_bar=True,
        )
        best_parameters = study.best_trial.params
        self.model = CatBoostRegressor(
                loss_function=f'MultiQuantile:alpha={quantile_str}',
                thread_count= 4,
                cat_features=["DMAR", "LD_INDL", "RF_CESAR", "SEX"],
                bootstrap_type =  "Bernoulli",
                sampling_frequency= 'PerTree',
                **best_parameters
            ).fit(
            x_train,
            y_train,
            eval_set=eval_dataset,
            use_best_model=True,
            early_stopping_rounds=20,
            plot=True,
        )


    def fit(
        self,
        x_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> None:
        self.autotune(x_train, x_test, y_train, y_test)

    def predict(self, df: pd.DataFrame) -> Tuple[PredictedProbas, PredictedClasses]:
        # predict Catboost classifier
        preds = self.model.predict(df)

        return preds


train_config = TrainingConfig()
train_config.global_random_state = i
train_config.calculate_shap_values = False
train_config.train_size = 0.8
train_config.enable_feature_selection = False
train_config.cat_encoding_via_ml_algorithm = True # use catboosts own cat encoding

catboost_model = CustomModel()

automl = BlueCastRegression(  # BlueCastCVRegression is not possible here, because the quantile regression predictions have an incompatible shape
        class_problem="regression",
        conf_training=train_config,
        ml_model=catboost_model,
        )
automl.fit(train.copy(), target_col=target) # fit_eval is not possible here, because the predictions have an incompatible shape
ml_models.append(automl)
```

Please note that custom ML models require user defined hyperparameter tuning. Pre-defined
configurations are not available for custom models.
Also note that the calculation of SHAP values only works with tree based models by
default. For other model architectures disable SHAP values in the TrainingConfig
via:

`train_config.calculate_shap_values = False`

Just instantiate a new instance of the TrainingConfig, update the param as above
and pass the config as an argument to the BlueCast instance during instantiation.
Feature importance can be added in the custom model definition.

#### Using the inbuilt ExperientTracker

For experimentation environments it can be useful to store all variables
and results from model runs.
BlueCast has an inbuilt experiment tracker to enhance the provided insights.
No setup is required. BlueCast will automatically store all necessary data
after each hyperparameter tuning trial.

```sh
# instantiate and train BlueCast
from bluecast.blueprints.cast import BlueCast

automl = BlueCast(
        class_problem="binary",
    )

automl.fit_eval(df_train, df_eval, y_eval, target_col="target")

# access the experiment tracker
tracker = automl.experiment_tracker

# see all stored information as a Pandas DataFrame
tracker_df = tracker.retrieve_results_as_df()
```

Now from here you could even feed selected columns back into a BlueCast
instance and try to predict the eval_score to check the get the feature
importance of your experiment data! Maybe you uncover hidden patterns
for your model training.

Please note that the number of stored experiments will probably be lower
than the number of started hyperparameter tuning trials. The experiment tracker
is skipped whenever Optuna prunes a trial.
The experiment triggers whenever the `fit` or `fit_eval` methods of a BlueCast
class instance are called (also within BlueCastCV). This means for custom
models the tracker will not trigger automatically and has to be added manually.

#### Gain insights across experiments

The inbuilt experiment tracker can be used to capture information across experiments:

* In non-CV instances it contains information about all hyperparameter tuning runs
* In CV instances it collects the same information across multiple model trainings
* It can be passed from one instance to another to collect information across several
runs:

```sh
# instantiate and train BlueCast
from bluecast.blueprints.cast import BlueCast

# train model 1
automl = BlueCast(
        class_problem="binary",
    )

automl.fit_eval(df_train, df_eval, y_eval, target_col="target")

# access the experiment tracker
tracker = automl.experiment_tracker

# pass experiment tracker to nd instance or training run
automl = BlueCast(
        class_problem="binary",
        experiment_tracker=tracker
    )
```

We can use the information to derive insights across model trainings:

```sh
from sklearn.ensemble import RandomForestRegressor
import shap

cols = [
    "shuffle_during_training",
    "global_random_state",
    "early_stopping_rounds",
    "autotune_model",
    "enable_feature_selection",
    "train_split_stratify",
    "use_full_data_for_final_model",
    "eta",
    "max_depth",
    "alpha",
    "lambda",
    "gamma",
    "max_leaves",
    "subsample",
    "colsample_bytree",
    "colsample_bylevel"
]

regr = RandomForestRegressor(max_depth=4, random_state=0)

tracker_df = tracker_df.loc[tracker_df["score_category"] == "oof_score"]

experiment_feats_df, experiment_feats_target = tracker_df.loc[:, cols], tracker_df.loc[:, "eval_scores"]

regr.fit(experiment_feats_df.fillna(0), experiment_feats_target.fillna(99))

explainer = shap.TreeExplainer(regr)


shap_values = explainer.shap_values(experiment_feats_df)
shap.summary_plot(shap_values, experiment_feats_df)
```

![SHAP experiment tracker](docs/source/shap_experiment_tracker.png)

Here it seems like random seeds had significant impact.

#### Use Mlflow via custom ExperientTracker API

The inbuilt experiment tracker is handy to start with, however in production
environments it might be required to send metrics to a Mlflow server or
comparable solutions. BlueCast allows to pass a custom experiment tracker.

```sh
# instantiate and train BlueCast
from bluecast.blueprints.cast import BlueCast
from bluecast.cnfig.base_classes import BaseClassExperimentTracker

class CustomExperimentTracker(BaseClassExperimentTracker):
    """Base class for the experiment tracker.

    Enforces the implementation of the add_results and retrieve_results_as_df methods.
    """

    @abstractmethod
    def add_results(
        self,
        experiment_id: int,
        score_category: Literal["simple_train_test_score", "cv_score", "oof_score"],
        training_config: TrainingConfig,
        model_parameters: Dict[Any, Any],
        eval_scores: Union[float, int, None],
        metric_used: str,
        metric_higher_is_better: bool,
    ) -> None:
        """
        Add results to the ExperimentTracker class.
        """
        pass # add Mlflow tracking i.e.

    @abstractmethod
    def retrieve_results_as_df(self) -> pd.DataFrame:
        """
        Retrieve results from the ExperimentTracker class
        """
        pass


experiment_tracker = CustomExperimentTracker()

automl = BlueCast(
        class_problem="binary",
        experiment_tracker=experiment_tracker,
    )

automl.fit_eval(df_train, df_eval, y_eval, target_col="target")

# access the experiment tracker
tracker = automl.experiment_tracker

# see all stored information as a Pandas DataFrame
tracker_df = tracker.retrieve_results_as_df()
```

#### Custom data drift checker

Since version 0.90 BlueCast checks for data drift for numerical
and categorical columns. The checks happen on the raw data.
Categories will be stored anonymized by default. Data drift
checks are not part of the model pipeline, but have to be called separately:

```sh
from bluecast.monitoring.data_monitoring import DataDrift


data_drift_checker = DataDrift()
# statistical data drift checks for numerical features
data_drift_checker.kolmogorov_smirnov_test(data, new_data, threshold=0.05)
# show flags
print(data_drift_checker.kolmogorov_smirnov_flags)

# statistical data drift checks for categorical features
data_drift_checker.population_stability_index(data, new_data)
# show flags
print(data_drift_checker.population_stability_index_flags)
# show psi values
print(data_drift_checker.population_stability_index_values)

# QQplot for two numerical columns
data_drift_checker.qqplot_two_samples(train["feature1"], test["feature1"], x_label="X", y_label="Y")
```

![QQplot example](docs/source/qqplot_sample.png)

### Model explainability

As BlueCast aims to support data scientist for real world applications,
it offers various insights around the model itself.

#### Hyperparameter tuning

After hyperparameter tuning the progress of the loss metric is shown.
This is useful to estimate if less tuning rounds would be sufficient
in future runs or if even more tuning rounds are required.

![Optuna loss progress example](docs/source/optuna_loss_progress.png)

Additionally, the most important hyperparameters are visualised. This can
be used to decide which parameters to include in an extra GridSearch layer.

![Optuna most important parameters example](docs/source/optuna_most_important_parameters.png)

#### Model performance

When building a model, knowing the model performance is crucial to make model
and business decisions. Therefore all BlueCast classes offer a `fit_eval` function,
that tunes and trains a model like the `fit` method, and evaluates the model
on unseen data. At the end a confusion matrix and a list of metrics are shown:

![Model performance metrics](docs/source/model_performance.png)

For CV classes the mean performance on all unseen dataset and the standard
deviation of those will be shown as well.

![Model performance CV metrics](docs/source/model_performance_cv.png)

#### SHAP values

While understanding the tuning process is helpful, we also want to understand
how the model behaves and which features are particularly important. Thus
BlueCast makes use of SHAP values. First it will show the global feature importance:

![SHAP global feature importance](docs/source/shap_global_importance.png)

Furthermore it will also show a sample on row level and plot waterfall plots of
SHAP values for each target clas of defined sample indices. User can change the
training config and adjust the `shap_waterfall_indices` parameter to pass a list
of indices instead.

![SHAP waterfall chart](docs/source/shap_waterfall_chart.png)

The third visualization is the dependence plot, which shows feature interactions
and their impact on SHAP values on a certain feature. By default BlueCast shows
dependence plots for the top 5 features for each class. The number of features
can adjusted via customization of the `show_dependence_plots_of_top_n_features`
param in the training config.

![SHAP dependence plot](docs/source/shap_dependence_plot.png)

The SHAP functions are part of all BlueCast classes and are called when using
the `fit` method.

This toolkit can also be used after model training for new data or for an external
model.

```python
from bluecast.evaluation.shap_values import (
    shap_dependence_plots,
    shap_explanations,
    shap_waterfall_plot,
)

shap_waterfall_indices = [2, 35, 999]
class_problem = "binary" # or 'multiclass' or 'regression'
show_dependence_plots_of_top_n_features = 5

shap_values, explainer = shap_explanations(automl.ml_model.model, x_test)

shap_waterfall_plot(
  explainer, shap_waterfall_indices, class_problem
)
shap_dependence_plots(
  shap_values,
  x_test,
  conf_training.show_dependence_plots_of_top_n_features,
)
```

### Conformal prediction

Over the past years conformal prediction gained increasing attention. It allows to
add uncertainty quantification around every model at the cost of just a bit of
additional computation.
In BlueCast we provide a model and architecture agnostic conformal prediction
wrapper that allows the usage of any class that has a `predict` or `predict_proba`
method.
For `BlueCast` and `BlueCastRegression` conformal prediction can be used after
the instance has been trained.

```sh
from bluecast.blueprints.cast import BlueCast
from sklearn.model_selection import train_test_split


# we leave it up to the user to split off a calibration set
X_train, X_calibrate, y_train, y_calibrate = train_test_split(
     X, y, test_size=0.33, random_state=42)

automl = BlueCast(
        class_problem="binary",
    )

X_train["target"] = y
automl.fit(X_train, target_col="target")

# make use of calibration
automl.calibrate(X_calibrate, y_calibrate)

# point prediction as usual
y_probs, y_classes = automl.predict(df_val)

# prediction sets
pred_sets = automl.predict_sets(df_val, alpha=0.05)

# prediction intervals
pred_intervals = automl.pred_interval(df_val)
```

### Plotting decision trees

How to plot decision trees will depend on the exact implementation. As BlueCast
uses Xgboost by default, we illustrate the default way.

#### Accessing the trained models

Regardless of the model architecture used we need to know where BlueCast stores
the trained model. The exact path differs between BlueCast(Regression) and
Bluecast(Regression)CV classes as CV classes are a wrapper around BlueCast classes.

##### BlueCast classes

The BlueCast classes store their model in an `ml_model` attribute where the trained
model is a `model` attribute.

```python
import matplotlib.pyplot as plt
from xgboost import plot_tree

plot_tree(automl.ml_model.model)
fig = plt.gcf()
fig.set_size_inches(150, 80)
plt.show()
```

![Xgboost tree](docs/source/xgboost_tree.png)

##### BlueCastCV classes

BlueCast have two characteristics to pay attention two:

* they are a wrapper around BlueCast classes
* they usually store multiple BlueCast instances at once

The BlueCast instances are stored inside a list attribute `bluecast_models`:

```python
import matplotlib.pyplot as plt
from xgboost import plot_tree

for model in automl.bluecast_models:
    plot_tree(model.ml_model.model)
    fig = plt.gcf()
    fig.set_size_inches(150, 80)
    plt.show()
```

This way we loop through all stored ml models and see the decision trees for each
of them. This can reveal significant differences in the trees.

![Xgboost tree](docs/source/xgboost_multi_tree.png)

## Convenience features

Despite being a lightweight library, BlueCast also includes some convenience
with the following features:

* automatic feature type detection and casting
* automatic DataFrame schema detection: checks if unseen data has new or
  missing columns
* categorical feature encoding (target encoding or directly in Xgboost)
* datetime feature encoding
* automated GPU availability check and usage for Xgboost
  a fit_eval method to fit a model and evaluate it on a validation set
  to mimic production environment reality
* functions to save and load a trained pipeline
* shapley values
* ROC AUC curve & lift chart
* warnings for potential misconfigurations

The fit_eval method can be used like this:

```sh
from bluecast.blueprints.cast import BlueCast

automl = BlueCast(
        class_problem="binary",
    )

automl.fit_eval(df_train, df_eval, y_eval, target_col="target")
y_probs, y_classes = automl.predict(df_val)
```

It is important to note that df_train contains the target column while
df_eval does not. The target column is passed separately as y_eval.

## Code quality

To ensure code quality, we use the following tools:

* various pre-commit libraries
* strong type hinting in the code base
* unit tests using Pytest

For contributors, it is expected that all pre-commit and unit tests pass.
For new features it is expected that unit tests are added.

## Documentation

Documentation is provided via [Read the Docs](https://bluecast.readthedocs.io/en/latest/)

## Kaggle competition results and example notebooks

Even though BlueCast has been designed to be a lightweight
automl framework, it still offers the possibilities to
reach very good performance. We tested BlueCast in Kaggle
competitions to showcase the libraries capabilities
feature- and performance-wise.

* ICR top 20% finish with over 6000 participants ([notebook](https://www.kaggle.com/code/thomasmeiner/icr-bluecast-automl-almost-bronze-ranks))
* An advanced example covering lots of functionalities ([notebook](https://www.kaggle.com/code/thomasmeiner/ps3e23-automl-eda-outlier-detection/notebook))
* PS3E23: Predict software defects top 12% finish ([notebook](https://www.kaggle.com/code/thomasmeiner/ps3e23-automl-eda-outlier-detection?scriptVersionId=145650820))
* PS3E25: Predict hardness of steel via regression ([notebook](https://www.kaggle.com/code/thomasmeiner/ps3e25-bluecast-automl?scriptVersionId=153347618))
* PS4E1: Bank churn top 13% finish ([notebook](https://www.kaggle.com/code/thomasmeiner/ps4e1-eda-feature-engineering-modelling?scriptVersionId=158121062))
* A comprehensive guide about BlueCast showing many capabilities ([notebook](https://www.kaggle.com/code/thomasmeiner/ps4e3-bluecast-a-comprehensive-overview))
* BlueCast using a custom Catboost model for quantile regression ([notebook](https://www.kaggle.com/code/thomasmeiner/birth-weight-with-bluecast-catboost))

## How to contribute

Contributions are welcome. Please follow the following steps:

* Create a new branch from develop branch
* Add your feature or fix
* Add unit tests for new features
* Run pre-commit checks and unit tests (using Pytest)
* Adjust the `docs/source/index.md` file
* Copy paste the content of the `docs/source/index.md` file into the
  `README.md` file
* Push your changes and create a pull request

If library or dev dependencies have to be changed, adjust the pyproject.toml.
For readthedocs it is also requited to update the
`docs/srtd_requirements.txt` file. Simply run:

```sh
poetry export --with dev -f requirements.txt --output docs/rtd_requirements.txt
```

If readthedocs will be able to create the documentation can be tested via:

```sh
poetry run sphinx-autobuild docs/source docs/build/html
```

This will show a localhost link containing the documentation.

## Meta

Creator: Thomas Meißner – [LinkedIn](https://www.linkedin.com/in/thomas-mei%C3%9Fner-m-a-3808b346)
