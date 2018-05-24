# icinga2-master

This role installs Icinga 2 and configures it for a generic master.
A new CA is initialized and a local certificate is signed using the CA.
A PostgreSQL database can be initialized (user and database) and the schema is automatically imported.
A couple of generic configuration files is created, but no checks, hosts, ....
[icinga2-config](https://github.com/stuvusIT/icinga2-config) is responsible for that.

However, a zone file for all hosts in the inventory is created.
Each host gets an Endpoint and a Zone consisting of only this endpoint.
The parent of this Zone is defined via the host variable `icinga2_parent_zone`.
This variable must point to an existing Ansible group.
All hosts in this group get assigned to a Zone by that name and won't be assigned to their own zones.
If a parent Zone has itself as its parent, it is assumed that this is the root Zone and it won't get a parent.

Additional, a global zone called `global-templates` is created.

## Requirements

Ubuntu

## Role Variables

| Name                                        | Default / Mandatory                                   | Description                                                                      |
|:--------------------------------------------|:-----------------------------------------------------:|:---------------------------------------------------------------------------------|
| `icinga2_user`                              | `nagios`                                              | User under which Icinga 2 is run                                                 |
| `icinga2_group`                             | `nagios`                                              | Group under which Icinga 2 is run                                                |
| `icinga2_features`                          | `[ checker, command, mainlog, notification, syslog ]` | A list of features to enable                                                     |
| `icinga2_constants`                         | `{}`                                                  | Dict of constants to set                                                         |
| `icinga2_configure_postgres`                | `true`                                                | Whether to configure a PostgreSQL user and database and import the schema        |
| `icinga2_postgres_login_host`               | `localhost`                                           | Host to connect to for setting up PostgreSQL                                     |
| `icinga2_postgres_login_user`               | `postgres`                                            | User to connect with for setting up PostgreSQL                                   |
| `icinga2_postgres_login_password`           |                                                       | Password to connect with for setting up PostgreSQL                               |
| `icinga2_postgres_user`                     | `icinga2`                                             | Name of the PostgreSQL user to create                                            |
| `icinga2_postgres_database`                 | `icinga2`                                             | Name of the PostgreSQL database to create                                        |
| `icinga2_feature_api_salt`                  | (:heavy_check_mark:)                                  | (Only when issuing certificates) Salt for certificate createion. Keep it secret! |
| `icinga2_feature_api_bind`                  | `0.0.0.0`                                             | Host to bind to for API requests                                                 |
| `icinga2_feature_api_port`                  | `5665`                                                | Port to bind to for API requests                                                 |
| `icinga2_feature_api_accept_config`         | `false`                                               | Whether to accept configurations via the API cluster                             |
| `icinga2_feature_api_accept_commands`       | `false`                                               | Whether to accept commands via the API cluster                                   |
| `icinga2_feature_api_tlsmin`                | `TLSv1.2`                                             | Minimum TLS version for API clients                                              |
| `icinga2_feature_checker_concurrent`        | `512`                                                 | Number of concurrent checks to execute                                           |
| `icinga2_feature_command_path`              | `/var/run/icinga2/cmd/icinga2.cmd`                    | Path to the command socket to create                                             |
| `icinga2_feature_idogpsql_host`             | `localhost`                                           | PostgreSQL host to connect to                                                    |
| `icinga2_feature_idogpsql_port`             | `5432`                                                | PostgreSQL port to connect to                                                    |
| `icinga2_feature_idogpsql_user`             | `icinga2`                                             | PostgreSQL user to connect with                                                  |
| `icinga2_feature_idogpsql_password`         | `icinga2`                                             | PostgreSQL password to connect with                                              |
| `icinga2_feature_idogpsql_database`         | `icinga2`                                             | PostgreSQL database to connect to                                                |
| `icinga2_feature_idogpsql_instance_name`    | `default`                                             | Name for this instance in the DB. Used for HA                                    |
| `icinga2_feature_idogpsql_ha`               | `true`                                                | Enable Icinga 2 HA in the database                                               |
| `icinga2_feature_idogpsql_failover_timeout` | `60s`                                                 | HA failover in the database                                                      |
| `icinga2_feature_idogpsql_cleanup`          | `{}`                                                  | Items to clean (key) and their maximum age (value)                               |
| `icinga2_feature_mainlog_severity`          | `information`                                         | Minimum log level for messages to be logged                                      |
| `icinga2_feature_mainlog_path`              | `/var/log/icinga2/icinga2.log`                        | Path to the mainlog                                                              |
| `icinga2_feature_notification_ha`           | `true`                                                | Whether to enable notification HA                                                |

## Example Playbook

```yml
- hosts: icinga
  roles:
    - role: icinga2-master
      icinga2_feature_api_salt: ieChahchaecei8zai1va
      icinga2_feature_idopgsql_ha: false
```

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Author Information

- [Janne Heß](https://github.com/dasJ)
