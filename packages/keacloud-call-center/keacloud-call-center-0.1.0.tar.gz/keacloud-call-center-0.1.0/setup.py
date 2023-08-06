from distutils.core import setup
setup(
    name='keacloud-call-center',
    packages=['keacloud-call-center'],  # this must be the same as the name above

    package_dir={"keacloud-call-center": "."},
    package_data={
        "keacloud-call-center": [
            "dist/*.css",
            "dist/*.js",
            "lib/*.css",
            "lib/*.js"
        ]
    },

    version='0.1.0',
    description='Frontend files package for keacloud-call-center',
    author='Diwank Tomer',
    author_email='diawnk@kea.cloud',
    url='https://github.com/keacloud/new-call-center',  # use the URL to the github repo
    keywords=['kea']
)
