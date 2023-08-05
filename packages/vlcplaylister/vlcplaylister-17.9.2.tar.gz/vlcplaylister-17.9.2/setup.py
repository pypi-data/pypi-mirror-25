from setuptools import setup

setup(
    name='vlcplaylister',
    version='17.09.2',
    entry_points={
        'console_scripts': [
            'playlister=playlister:main',
        ],
    },
    description='VLC Playlist generater',
    long_description=open('README').read(),
    url='https://github.com/compmonk/playlister',
    author='compmonk',
    license='MIT',
    keywords='vlc videos videos-series tv-series tv-shows playlist vlc-playlist',
)
