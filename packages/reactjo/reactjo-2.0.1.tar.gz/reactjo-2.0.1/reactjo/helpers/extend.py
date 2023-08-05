import os, subprocess

def extend():
    src = 'https://github.com/aaron-price/reactjo-extension-template.git'
    target = os.getcwd()
    rc_home = ""
    out_home = ""

    while rc_home == "":
        rc_home = input("Please name your extension (e.g. reactjo_django): ")
    while out_home == "":
        out_home = input("What will the main output directory be called (e.g. backend, frontend, etc): ")

    ext_path = target + '/' + rc_home
    subprocess.run([ 'git', 'clone', src, rc_home ])

    os.chdir(os.path.join(rc_home))
    subprocess.run(['git','remote', 'rm', 'origin'])

    # Update the extension_constants
    extension_constants_string = """
        # file_manager('$out/some/path') == 'super_root/project_path/{out}/some/path'
        OUTPUT_HOME = '{out}'

        # file_manager('$rc/assets') == 'super_root/reactjorc/extensions/{rc}/assets'
        RC_HOME = '{rc}'
    """.format(
        out=out_home,
        rc=rc_home
    ).replace('    ','')
    extension_constants_path = os.path.join('helpers/extension_constants.py')
    file = open(extension_constants_path, 'w')
    file.write(extension_constants_string)
    file.close()

    # Fill in the readme constants
    readme_path = os.path.join('README.md')
    readme_file = open(readme_path, 'r').read()
    readme_file = readme_file.replace('extension_name_here', rc_home)
    file = open(readme_path, 'w')
    file.write(readme_file)
    file.close()

    # Fill in the 'writing an extension' constants
    readme_path = os.path.join('WRITING_AN_EXTENSION.md')
    readme_file = open(readme_path, 'r').read()
    readme_file = readme_file.replace('extension_name_here', rc_home)
    file = open(readme_path, 'w')
    file.write(readme_file)
    file.close()
