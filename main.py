import os
import subprocess
from user_input.main import *

def search_conan_package(package_name):
    print(f"Searching for package '{package_name}' in conan center...")
    subprocess.run(["conan", "search", package_name, "-r", "conancenter"])

def load_existing_conanfile(conanfile_path):
    packages = []
    if not os.path.exists(conanfile_path):
        return packages

    in_requires_section = False
    with open(conanfile_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "[requires]":
                in_requires_section = True
            elif stripped.startswith("[") and stripped.endswith("]"):
                in_requires_section = False
            elif in_requires_section and stripped:
                packages.append(stripped)

    return packages

def create_conanfile(root_dir):
    conanfile_path = os.path.join(root_dir, "conanfile.txt")
    packages = load_existing_conanfile(conanfile_path)

    if packages:
        print("Loaded existing packages from conanfile.txt:")
        for package in packages:
            print(f" - {package}")

    quick_select = get_yes_no("Before we get started, would you like to choose from a selection of commonly used packages to speed up the process?")

    if quick_select:
        quick_selected_packages = select_options([
            "glfw/3.4",
            "glad/0.1.36",
            "fmt/11.2.0",
            "spdlog/1.14.1",
            "glm/cci.20230113",
            "stb/cci.20240531",
            "nlohmann_json/3.11.3",
            "assimp/5.4.3",
            "enet/1.3.18",
            "openal-soft/1.23.1",
            "libsndfile/1.2.2"
        ])
        for pkg in quick_selected_packages:
            if pkg not in packages:
                packages.append(pkg)

    requires_more_dependencies = True
    if quick_select:
        requires_more_dependencies = get_yes_no("Do you require further dependencies?")

    if requires_more_dependencies:
        print("Conan package management:")
        print("Use 'search <package>' to search for packages.")
        print("Use 'add <package/version>' to add a package to your project.")
        print("Use 'remove <package/version>' to remove a package from your project.")
        print("Type 'done' when you are finished.")

        while True:
            user_input = input("> ").strip()
            if user_input.lower() == "done":
                break
            elif user_input.startswith("search "):
                package_name = user_input[len("search "):].strip()
                if package_name:
                    search_conan_package(package_name)
            elif user_input.startswith("add "):
                package = user_input[len("add "):].strip()
                if package and package not in packages:
                    packages.append(package)
                    print(f"Added package '{package}'")
            elif user_input.startswith("remove "):
                package = user_input[len("remove "):].strip()
                if package in packages:
                    packages.remove(package)
                    print(f"Removed package '{package}'")
            else:
                print("Invalid command. Please use 'search', 'add', 'remove', or 'done'.")

    if packages:
        with open(conanfile_path, "w") as f:
            f.write("[requires]\n")
            for package in packages:
                f.write(f"{package}\n")
            f.write("\n[generators]\nCMakeDeps\nCMakeToolchain\n\n[layout]\ncmake_layout")
        print(f"\nUpdated conanfile.txt in {root_dir} with the following packages:")
        for package in packages:
            print(f" - {package}")
    else:
        print("No packages were added. Skipping conanfile.txt creation.")
