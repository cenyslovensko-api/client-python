from setuptools import setup

from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):
    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self) -> tuple[str, str, str]:
        _, _, platform_tag = super().get_tag()
        if platform_tag == "linux_x86_64":
            platform_tag = "manylinux2014_x86_64"
        elif platform_tag == "linux_aarch64":
            platform_tag = "manylinux2014_aarch64"
        return "py3", "none", platform_tag


setup(cmdclass={"bdist_wheel": bdist_wheel})
