import PyInstaller.__main__
import distutils.dir_util
import shutil


def main():


    from_dir = "../SUB3/resources"
    to_dir = "./LETREP2/resources"
    distutils.dir_util.copy_tree(from_dir, to_dir)

    PyInstaller.__main__.run([
        '../SUB3/main.py',
        '--onefile',
        '--windowed',
        '--distpath',
        './LETREP2/',
        '--icon',
        './LetRep 2_Logo.ico',
        '--name',
        'LETREP2 Software',
    ])

    PyInstaller.__main__.run([
        './installer.py',
        '--onefile',
        '--windowed',
        '--distpath',
        './LETREP2/'
    ])


    shutil.make_archive("LETREP2_Installer", 'zip', "./LETREP2")

    shutil.rmtree("LETREP2")
if __name__ == "__main__":
    main()
