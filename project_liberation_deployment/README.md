# project-liberation-deployment

Scripts and configuration for project-liberation deployment.

## Cloning the repositories

All below steps/instructions require local copies of `project-liberation` and `project-liberation-config` repositories.

## Deployment

### Prerequisites

#### Ansible

You need `ansible` package to run configuration playbooks. Install it from your system package manager.

### Configuring `project-liberation` machine

This step configures machine for project-liberation app.

```bash
 cd project-liberation/project_liberation_deployment/
ansible-playbook configure.yml                                    \
    --inventory ../../project-liberation-config/ansible_inventory \
    --user      $user
```

### Deploying `project-liberation` machine

There's few options to execute this step. Update project-liberation application to master version as a default.
To control version of project-liberation set the `$project_liberation_version` shell variable.
Additional options:
- `$upload_secret_file` - this option requires knowledge of vault password and using additional `--ask-vault-pass` flag
- `$upload_image_package` - this option requires local images package with name `project-liberation.zip` placed in the `../../project-liberation-image-packages` directory
- `$generate_static_files`
- `$migrate_database`

To execute additional options set shell variables to `yes` value.

```bash
cd project-liberation/project_liberation_deployment/
ansible-playbook deploy.yml                                             \
    --extra-vars project_liberation_version=$project_liberation_version \
    --extra-vars upload_secret_file=$upload_secret_file                 \
    --extra-vars upload_image_package=$upload_image_package             \
    --extra-vars generate_static_files=$generate_static_files           \
    --extra-vars migrate_database=$migrate_database                     \
    --inventory  ../../project-liberation-config/ansible_inventory      \
    --user       $user
```

