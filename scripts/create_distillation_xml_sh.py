import argparse
import os
import jinja2
import yaml
from yml_to_xml import eigs_xml,perams_xml,meson_xml,baryon_xml,chroma_sh_xml

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
print(PROJECT_DIR)
FDIR = os.path.dirname(os.path.realpath(__file__))
INFILES = os.path.abspath(os.path.join(FDIR, "ens_files"))
TEMPLATE = os.path.join(FDIR,'templates')
RESULTPATH = os.path.join(FDIR,'res')
XMLPATH= os.path.join(RESULTPATH,'xml')
SHPATH= os.path.join(RESULTPATH,'sh')
OUTPATH = os.path.join(RESULTPATH,'out')
LOGPATH = os.path.join(RESULTPATH,'log')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file',type=str)
    parser.add_argument('--cfg_i', type=int)
    parser.add_argument('--cfg_f', type=int)
    parser.add_argument('--cfg_step', type=int, nargs='?', default=10, help='default: %(default)s')
    parser.add_argument('--chroma_type',type=str,help='choose regular or superb chroma task type')
    parser.add_argument('--overwrite', type=bool, nargs='?', default=False, help='if true, overwrite existing xml and sh scripts for chroma task of interest')
    parser.add_argument('--metaq',type=bool,default=True)
    parser.add_argument('--combined',default='False',help='if true, generate a combined xml for all chroma tasks')
    parser.add_argument('--eig_dir', default='/res/eigs', help='change this default option when we decide where to store the eigenbasis on disk')
    parser.add_argument('--cfg_path', default='/p/project/exotichadrons/pederiva/6stout/beta_3.70/ms_0.000/mud_-0.022/s32t96/cnfg/', help='default: %(default)s')
    parser.add_argument('--code_dir', default='/p/scratch/exotichadrons/pederiva/chroma-distillation', help='default: %(default)s')
    parser.add_argument('--job_name', default='distillation', help='default: %(default)s')
    parser.add_argument('--run_dir', default='', help='default: %(default)s')
    parser.add_argument('--quda_resource_path', default='/p/scratch/exotichadrons/pederiva/chroma-distillation/quda_resources/', help='default: %(default)s')
    # parser.add_argument('--start_METAQ',default='y')? put eigs into metaq priority 
    # if eigs work is done, 
     
    options = parser.parse_args()

    with open(os.path.join(options.in_file)) as f:
        dataMap = yaml.safe_load(f)

    missing_values = [key for key in ['run_path','job_name','cfg_path'] if key not in dataMap]

    if missing_values:
        for key in missing_values:
            value = input(f"you forgot to include '{key}' in your infile dummy!: ")
            dataMap[key] = value

        # Rewrite the YAML file with added values
        with open(options.in_file, 'w') as f:
            yaml.safe_dump(dataMap, f)

    # Set up Jinja.
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE),undefined=jinja2.StrictUndefined)
    # if options.chroma_type==''
    template_eigs = env.get_template('eigs_regular.jinja.xml')
    template_perams = env.get_template('peram.jinja.xml')
    template_meson = env.get_template('meson.jinja.xml')
    template_baryon = env.get_template('baryon.jinja.xml')
    template_chroma_eigs = env.get_template('eigs_juwels.sh.j2')
    template_chroma_perams = env.get_template('peram_juwels.sh.j2')
    template_chroma_meson = env.get_template('meson_juwels.sh.j2')
    template_chroma_baryon = env.get_template('baryon_juwels.sh.j2')


    objects = ['eigs', 'perams', 'meson', 'baryon','chroma_eigs','chroma_perams','chroma_meson','chroma_baryon']
    run_objects = []
    if dataMap['run_eigs']:
       run_objects.append('eigs')
       run_objects.append('chroma_eigs')

    if dataMap['run_perams']:
       run_objects.append('perams')
       run_objects.append('chroma_perams')

    if dataMap['run_meson']:
       run_objects.append('meson')
       run_objects.append('chroma_meson')

    if dataMap['run_baryon']:
       run_objects.append('baryon')
       run_objects.append('chroma_baryon')

    templates = {
        'eigs': template_eigs,
        'perams': template_perams,
        'meson': template_meson,
        'baryon': template_baryon,
        'chroma_eigs': template_chroma_eigs,
        'chroma_perams': template_chroma_perams,
        'chroma_meson': template_chroma_meson,
        'chroma_baryon': template_chroma_baryon
    }
    xml_classes = {
        'eigs': eigs_xml.Eigs,
        'perams': perams_xml.Perams,
        'meson': meson_xml.Meson,
        'baryon': baryon_xml.Baryon,
        'chroma_eigs': chroma_sh_xml.ChromaOptions,
        'chroma_meson': chroma_sh_xml.ChromaOptions,
        'chroma_perams': chroma_sh_xml.ChromaOptions,
        'chroma_baryon': chroma_sh_xml.ChromaOptions

    }

    for cfg_id in range(options.cfg_i,options.cfg_f,options.cfg_step):
        print('Creating scripts for configuration', cfg_id)
        for flavor, beta, quarktype in [('light', 0.022, 'ud'),
                                        ('strange', 0.000, 's')]:
            cfg_dir = os.path.realpath(os.path.join('..','ini','cnfg{:02d}'.format(cfg_id)))
            # os.makedirs(os.path.join(cfg_dir, 'outputs'), exist_ok=True)
            rundir = os.path.join(options.run_dir, cfg_dir)
            # jobname = '{}_{}'.format(options['jobname'], quarktype)
            
            outfile = '../outputs/run_{:02d}.out'.format(cfg_id)

            for obj in run_objects:
                obj_dir = os.path.join(cfg_dir)
                os.makedirs(obj_dir, exist_ok=True)

                if obj.startswith('chroma'):
                    ini_out = '{}_{:02d}.sh'.format(obj.split('_')[1], cfg_id)
                else:
                    ini_out = '{}_{:02}.ini.xml'.format(obj, cfg_id)

                ini_out_path = os.path.join(obj_dir,ini_out)
                if not os.path.exists(ini_out_path) or options.overwrite:

                    with open(os.path.join(options.in_file)) as f:
                        dataMap = yaml.safe_load(f)

                    if dataMap.get(f"run_{obj}",True):
                        base = xml_classes[obj]
                        # pydantic versioning 
                        if dataMap['facility'] in ['jureca','juwels']:
                            expected_keys = base.__fields__.keys()
                        else:
                            expected_keys = base.model_fields.keys()
                        filtered_data = {k: v for k, v in dataMap.items() if k in expected_keys}
                        filtered_data['cfg_id'] = '{:02d}'.format(cfg_id)
                        ens_props = chroma_sh_xml.parse_ensemble(short_tag=filtered_data['ens_short'])
                        filtered_data.update(ens_props)

                        output_xml = templates[obj].render(filtered_data)
                        with open(ini_out_path, 'w') as f:
                            f.write(output_xml)
                        if options.metaq and ini_out_path.endswith('.sh'):
                            os.symlink(ini_out_path,os.path.join(filtered_data['metaq_dir'],'priority',ini_out))
                            
                else:
                    print(f"File {ini_out_path} already exists. Skipping file generation.")


    os.makedirs(LOGPATH, exist_ok=True)
    os.makedirs(OUTPATH, exist_ok=True)

if __name__ == '__main__':
    main()


