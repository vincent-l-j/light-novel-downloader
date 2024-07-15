# Project Template with Automated Workflows

Welcome to the Project Template repository!
This repository serves as a template for new projects.
It comes with automated workflows to streamline development processes.
Below, you'll find information on how to get started and details about the automated workflows in place.

## Getting Started

1. **Create a repo from this Template Repository**

   ```bash
   gh repo create <new-repo-name> --template="<link-to-template-repo>"
   # OR
   gh repo create <new-repo-name> --template="<owner/template-repo>"
   ```

## Automated Workflows

### 1. Changelog Generation

We automatically generate a changelog based on commit messages using the
[Release Please](https://github.com/google-github-actions/release-please-action)
GitHub Action.
The Release Please GitHub Action opens or updates a pull request that will:

- Bump the version following Semantic Versioning (SemVer).
- Generate or update the changelog.
- Create a new commit and tag for the release.

### 2. Pull Request Template and Title Enforcement

When creating a pull request, make sure to follow the template provided.
Additionally, we enforce specific rules for pull request titles.
The template and title checks are automated using GitHub Actions.

## License

This project is licensed under the [MIT License](LICENSE.md).

Thank you for using the Project Template!
If you have any questions or encounter issues, please open an
[issue](https://github.com/vincent-l-j/project-template/issues).
