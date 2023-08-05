from contextlib import contextmanager
import logging
import os
import timeit
import time

from mdt import get_processing_strategy
from mdt.utils import model_output_exists, load_samples, per_model_logging_context
from mdt.processing_strategies import SamplingProcessor, SaveAllSamples, \
    SaveNoSamples, SaveThinnedSamples, get_full_tmp_results_path
from mdt.exceptions import InsufficientProtocolError


__author__ = 'Robbert Harms'
__date__ = "2015-05-01"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def sample_composite_model(model, input_data, output_folder, sampler, tmp_dir,
                           recalculate=False, store_samples=True,
                           initialization_data=None):
    """Sample a composite model.

    Args:
        model (:class:`~mdt.models.composite.DMRICompositeModel`): a composite model to sample
        input_data (:class:`~mdt.utils.MRIInputData`): The input data object with which the model
            is initialized before running
        output_folder (string): The full path to the folder where to place the output
        sampler (:class:`mot.cl_routines.sampling.base.AbstractSampler`): The sampling routine to use.
        tmp_dir (str): the preferred temporary storage dir
        recalculate (boolean): If we want to recalculate the results if they are already present.
        store_samples (boolean or int): if set to False we will store none of the samples. If set to an integer we will
            store only thinned samples with that amount.
        initialization_data (:class:`~mdt.utils.InitializationData`): provides (extra) initialization data to use
            during model fitting. If we are optimizing a cascade model this data only applies to the last model in the
            cascade.
    """
    if store_samples:
        if isinstance(store_samples, int):
            sample_to_save_method = SaveThinnedSamples(store_samples)
        else:
            sample_to_save_method = SaveAllSamples()
    else:
        sample_to_save_method = SaveNoSamples()

    if not model.is_protocol_sufficient(input_data.protocol):
        raise InsufficientProtocolError(
            'The provided protocol is insufficient for this model. '
            'The reported errors where: {}'.format(model.get_protocol_problems(input_data.protocol)))

    logger = logging.getLogger(__name__)

    if not recalculate:
        if model_output_exists(model, output_folder + '/univariate_statistics/', append_model_name_to_path=False):
            logger.info('Not recalculating {} model'.format(model.name))
            return load_samples(output_folder)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    model.set_input_data(input_data)

    with per_model_logging_context(output_folder, overwrite=recalculate):
        if initialization_data:
            logger.info('Preparing the model with the user provided initialization data.')
            initialization_data.apply_to_model(model, input_data)

        with _log_info(logger, model.name):
            worker = SamplingProcessor(
                sampler, model, input_data.mask, input_data.nifti_header, output_folder,
                get_full_tmp_results_path(output_folder, tmp_dir), recalculate,
                samples_to_save_method=sample_to_save_method)

            processing_strategy = get_processing_strategy('sampling')
            processing_strategy.process(worker)


@contextmanager
def _log_info(logger, model_name):
    minimize_start_time = timeit.default_timer()
    logger.info('Sampling {} model'.format(model_name))
    yield
    run_time = timeit.default_timer() - minimize_start_time
    run_time_str = time.strftime('%H:%M:%S', time.gmtime(run_time))
    logger.info('Sampled {0} model with runtime {1} (h:m:s).'.format(model_name, run_time_str))
