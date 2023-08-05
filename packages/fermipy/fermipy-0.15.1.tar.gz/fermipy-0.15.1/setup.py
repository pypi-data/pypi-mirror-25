#!/usr/bin/env python
from setuptools import setup, find_packages
from fermipy.version import get_git_version

setup(
    name='fermipy',
    version=get_git_version(),
    author='The Fermipy developers',
    author_email='fermipy.developers@gmail.com',
    description='A Python package for analysis of Fermi-LAT data',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/fermiPy/fermipy",
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Development Status :: 4 - Beta',
    ],
    scripts=[],
    entry_points={'console_scripts': [
        'fermipy-dispatch = fermipy.scripts.dispatch:main',
        'fermipy-clone-configs = fermipy.scripts.clone_configs:main',
        'fermipy-collect-sources = fermipy.scripts.collect_sources:main',
        'fermipy-cluster-sources = fermipy.scripts.cluster_sources:main',
        'fermipy-flux-sensitivity = fermipy.scripts.flux_sensitivity:main',
        'fermipy-intensity-map = fermipy.scripts.intensity_map:main',
        'fermipy-run-tempo = fermipy.scripts.run_tempo:main',
        'fermipy-healview = fermipy.scripts.HEALview:main',
        'fermipy-select = fermipy.scripts.select_data:main',
        'fermipy-preprocess = fermipy.scripts.preprocess_data:main',
        'fermipy-validate = fermipy.scripts.validate:main',
        'fermipy-quick-analysis = fermipy.scripts.quickanalysis:main',
        'fermipy-coadd = fermipy.scripts.coadd:main',
        'fermipy-vstack = fermipy.scripts.vstack_images:main',
        'fermipy-gtexcube2-sg = fermipy.diffuse.job_library:invoke_sg_gtexpcube2',
        'fermipy-sum-ring-gasmaps-sg = fermipy.diffuse.job_library:invoke_sg_sum_ring_gasmaps',
        'fermipy-vstack-diffuse-sg = fermipy.diffuse.job_library:invoke_sg_vstack_diffuse',
        'fermipy-healview-diffuse-sg = fermipy.diffuse.job_library:invoke_sg_healview_diffuse',
        'fermipy-srcmaps-catalog-sg = fermipy.diffuse.job_library:invoke_sg_gtsrcmaps_catalog',
        'fermipy-split-and-bin = fermipy.diffuse.gt_split_and_bin:main_single',
        'fermipy-split-and-bin-sg = fermipy.diffuse.gt_split_and_bin:main_batch',
        'fermipy-split-and-mktime = fermipy.diffuse.gt_split_and_mktime:main_single',
        'fermipy-split-and-mktime-sg = fermipy.diffuse.gt_split_and_mktime:main_batch',
        'fermipy-coadd-split = fermipy.diffuse.gt_coadd_split:main',
        'fermipy-srcmaps-diffuse = fermipy.diffuse.gt_srcmap_partial:main_single',
        'fermipy-srcmaps-diffuse-sg = fermipy.diffuse.gt_srcmap_partial:main_batch',
        'fermipy-merge-srcmaps = fermipy.diffuse.gt_merge_srcmaps:main_single',
        'fermipy-merge-srcmaps-sg = fermipy.diffuse.gt_merge_srcmaps:main_batch',
        'fermipy-init-model = fermipy.diffuse.gt_assemble_model:main_init',
        'fermipy-assemble-model = fermipy.diffuse.gt_assemble_model:main_single',
        'fermipy-assemble-model-sg = fermipy.diffuse.gt_assemble_model:main_batch',
        'fermipy-residual-cr = fermipy.diffuse.residual_cr:main_single',
        'fermipy-residual-cr-sg = fermipy.diffuse.residual_cr:main_batch',
        'fermipy-residual-cr-chain = fermipy.diffuse.residual_cr:main_chain',
        'fermipy-catalog-chain = fermipy.diffuse.catalog_src_manager:main_chain',
        'fermipy-diffuse-chain = fermipy.diffuse.diffuse_src_manager:main_chain',
        'fermipy-diffuse-analysis = fermipy.diffuse.diffuse_analysis:main_chain',
        'fermipy-gtexphpsun-sg = fermipy.diffuse.solar:invoke_sg_Gtexphpsun',
        'fermipy-gtsuntemp-sg = fermipy.diffuse.solar:invoke_sg_Gtsuntemp',
        'fermipy-sunmoon = fermipy.diffuse.solar:main',
        'fermipy-job-archive = fermipy.jobs.job_archive:main_browse',
        'fermipy-file-archive = fermipy.jobs.file_archive:main_browse',
    ]},
    install_requires=[
        'numpy >= 1.6.1',
        'astropy >= 1.2.1',
        'matplotlib >= 1.5.0',
        'scipy >= 0.14',
        'pyyaml',
        'healpy',
        'wcsaxes',
    ],
    extras_require=dict(
        all=[],
    ),
)
