#!/usr/bin/env python3
import optparse
from pathlib import Path
from zenodo_get import download

catalogues = {'GWTC-2.1':   "10.5281/zenodo.5117702",
              'GWTC-3.0':   "10.5281/zenodo.5546662",
              'GWTC-4.0':   "10.5281/zenodo.16053483",
              'GWTC-4.1':   "10.5281/zenodo.20275768",
              'GWTC-5.0-1': "10.5281/zenodo.20276105",
              'GWTC-5.0-2': "10.5281/zenodo.20291739",
              }

injections = {'GWTC-3': "10.5281/zenodo.5636815",
              'GWTC-4': "10.5281/zenodo.16740127",
              'GWTC-5': "10.5281/zenodo.19500051",
            }

inj_names = {'GWTC-3': "o1+o2+o3_mixture_real+semianalytic-LIGO-T2100377-v2.hdf5",
             'GWTC-4': "mixture-semi_o1_o2-real_o3_o4a-cartesian_spins_20250503134659UTC.hdf",
             'GWTC-5': "mixture-semi_o1_o2-real_o3_o4a_o4b-cartesian_spins_20260410130052UTC-clipped.hdf",
             }

def _rename_events(evs_folder):
    # Rename events
    for file in evs_folder.glob('*.h*5'):
        n = file.name
        idx = n.index('GW')
        new_name = 'GW'+n.split('GW')[-1][:13]+file.suffix
        file.rename(Path(file.parents[0],new_name))

def _make_symlink(file, evs_folder, out_folder = '.'):
    name = file.stem
    cat_folder = Path(out_folder, name)
    if not cat_folder.exists():
        cat_folder.mkdir(parents=True)
    with open(file, 'r') as w:
        ll = [line.rstrip() for line in w]
    for l in ll:
        if len(l) > 0:
            Path(cat_folder, l).symlink_to(Path(evs_folder, l))

def get_data():
    
    parser = optparse.OptionParser(prog = 'gwget', description = 'Automatic downloader of LVK GW posterior samples')
    # Input/output
    parser.add_option("-o", "--output", type = "string", dest = "output", help = "Output folder. Default: run directory", default = '.')
    parser.add_option("-c", "--catalogue", type = "choice", dest = "catalogue", help = "The catalogue to download", choices = ['GWTC-2', 'GWTC-3', 'GWTC-4', 'GWTC-5'], default = 'GWTC-5')
    parser.add_option("--no_injections", dest = "injections", action = 'store_false', help = "Skip injection download", default = True)
    
    (options, args) = parser.parse_args()
    
    # Folders
    output_folder = Path(options.output).resolve()
    if not output_folder.exists():
        output_folder.mkdir(parents=True)
    evs_folder = Path(output_folder, 'all_events')
    if not evs_folder.exists():
        evs_folder.mkdir(parents=True)
    inj_folder = Path(output_folder, 'injections')
    if not inj_folder.exists():
        inj_folder.mkdir(parents=True)
    lists_folder = Path(Path(__file__).parent.resolve(), 'lists')

    # Download events
    cat = options.catalogue

    download(record_or_doi = catalogues['GWTC-2.1'], file_glob = '*_mixed_cosmo.h5', output_dir = evs_folder)
    _rename_events(evs_folder)

    if ((cat == 'GWTC-3') or (cat == 'GWTC-4') or (cat == 'GWTC-5')):
        download(record_or_doi = catalogues['GWTC-3.0'], file_glob = '*_mixed_cosmo.h5', output_dir = evs_folder)
        if options.injections:
            download(record_or_doi = injections['GWTC-3'], file_glob = inj_names['GWTC-3'], output_dir = inj_folder)
            # Rename injections
            Path(inj_folder, inj_names['GWTC-3']).replace(Path(inj_folder, 'GWTC-3_injections.hdf5'))
        _rename_events(evs_folder)
        _make_symlink(Path(lists_folder,'gwtc3pop_bbh.txt'), evs_folder, output_folder)

    if ((cat == 'GWTC-4') or (cat == 'GWTC-5')):
        download(record_or_doi = catalogues['GWTC-4.1'], file_glob = '*PEDataRelease.hdf5', output_dir = evs_folder)
        if options.injections:
            download(record_or_doi = injections['GWTC-4'], file_glob = inj_names['GWTC-4'], output_dir = inj_folder)
            # Rename injections
            Path(inj_folder, inj_names['GWTC-4']).replace(Path(inj_folder, 'GWTC-4_injections.hdf5'))
        _rename_events(evs_folder)
        _make_symlink(Path(lists_folder,'gwtc4pop_bbh.txt'), evs_folder, output_folder)
            
    if (cat == 'GWTC-5'):
        download(record_or_doi = catalogues['GWTC-5.0-1'], file_glob = '*PEDataRelease.hdf5', output_dir = evs_folder)
        download(record_or_doi = catalogues['GWTC-5.0-2'], file_glob = '*PEDataRelease.hdf5', output_dir = evs_folder)
        if options.injections:
            download(record_or_doi = injections['GWTC-5'], file_glob = inj_names['GWTC-5'], output_dir = inj_folder)
            # Rename injections
            Path(inj_folder, inj_names['GWTC-5']).replace(Path(inj_folder, 'GWTC-5_injections.hdf5'))
        _rename_events(evs_folder)
        _make_symlink(Path(lists_folder,'gwtc5pop_bbh.txt'), evs_folder, output_folder)

def make_symlink_cat():
    
    parser = optparse.OptionParser(prog = 'makecat', description = 'Create symlink subcatalogue')
    # Input/output
    parser.add_option("-e", "--evs", type = "string", dest = "events", help = "Folder with events", default = None)
    parser.add_option("-l", "--list", type = "string", dest = "list", help = "List with events", default = None)
    
    (options, args) = parser.parse_args()
    
    if options.events is None:
        raise Exception("Please provide the path to all_events")
        
    if options.list is None:
        raise Exception("Please provide a list of events")

    file = Path(options.list).resolve()
    evs_folder = Path(options.events).resolve()
    _make_symlink(file, evs_folder)
