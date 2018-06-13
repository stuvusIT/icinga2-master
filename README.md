# icinga2-master

This role installs Icinga 2 and configures it for a master.
A new CA is initialized and a local certificate is signed using the CA.
A PostgreSQL database can be initialized (user and database) and the schema is automatically imported.
All configuration files, including checks, hosts, and notifications are created.

A zone file for all hosts in the inventory is created.
Each host gets an Endpoint and a Zone consisting of only this endpoint.
The parent of this Zone is defined via the host variable `icinga2_parent_zone`.
This variable must point to an existing Ansible group.
All hosts in this group get assigned to a Zone by that name and won't be assigned to their own zones.
If a parent Zone has itself as its parent, it is assumed that this is the root Zone and it won't get a parent.

Additionaly, a global zone called `global-templates` is created.

Hosts are automatically generated from your inventory.
You can use `icinga2_forwarded_vars` to include hostvars into the custom vars section of the Icinga 2 hosts.
Each host **must** have an `description` attribute that holds the description of the host.
Addutionally, `ansible_host` is filled in as the `address` of the Icinga 2 host.
If the zone is in the group specified by `icinga2_noagent_group`, the hostalive check is chosen for the host.
If not, the check specified by `icinga2_agent_check` is performed.
All Ansible groups are automatically converted into Icinga 2 groups.
Descriptions can be given using the `icinga2_host_groups` dict.

## Requirements

Ubuntu or Debian

## Role Variables

| Name                                        | Default / Mandatory                                   | Description                                                                                                              |
|:--------------------------------------------|:-----------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------|
| `icinga2_user`                              | `nagios`                                              | User under which Icinga 2 is run                                                                                         |
| `icinga2_group`                             | `nagios`                                              | Group under which Icinga 2 is run                                                                                        |
| `icinga2_features`                          | `[ checker, command, mainlog, notification, syslog ]` | A list of features to enable                                                                                             |
| `icinga2_constants`                         | `{}`                                                  | Dict of constants to set                                                                                                 |
| `icinga2_configure_postgres`                | `true`                                                | Whether to configure a PostgreSQL user and database and import the schema                                                |
| `icinga2_postgres_login_host`               | `localhost`                                           | Host to connect to for setting up PostgreSQL                                                                             |
| `icinga2_postgres_login_user`               | `postgres`                                            | User to connect with for setting up PostgreSQL                                                                           |
| `icinga2_postgres_login_password`           |                                                       | Password to connect with for setting up PostgreSQL                                                                       |
| `icinga2_postgres_user`                     | `icinga2`                                             | Name of the PostgreSQL user to create                                                                                    |
| `icinga2_postgres_database`                 | `icinga2`                                             | Name of the PostgreSQL database to create                                                                                |
| `icinga2_feature_api_salt`                  | (:heavy_check_mark:)                                  | (Only when issuing certificates) Salt for certificate creation. Keep it secret!                                          |
| `icinga2_feature_api_bind`                  | `0.0.0.0`                                             | Host to bind to for API requests                                                                                         |
| `icinga2_feature_api_port`                  | `5665`                                                | Port to bind to for API requests                                                                                         |
| `icinga2_feature_api_accept_config`         | `false`                                               | Whether to accept configurations via the API cluster                                                                     |
| `icinga2_feature_api_accept_commands`       | `false`                                               | Whether to accept commands via the API cluster                                                                           |
| `icinga2_feature_api_tlsmin`                | `TLSv1.2`                                             | Minimum TLS version for API clients                                                                                      |
| `icinga2_feature_checker_concurrent`        | `512`                                                 | Number of concurrent checks to execute                                                                                   |
| `icinga2_feature_command_path`              | `/var/run/icinga2/cmd/icinga2.cmd`                    | Path to the command socket to create                                                                                     |
| `icinga2_feature_idogpsql_host`             | `localhost`                                           | PostgreSQL host to connect to                                                                                            |
| `icinga2_feature_idogpsql_port`             | `5432`                                                | PostgreSQL port to connect to                                                                                            |
| `icinga2_feature_idogpsql_user`             | `icinga2`                                             | PostgreSQL user to connect with                                                                                          |
| `icinga2_feature_idogpsql_password`         | `icinga2`                                             | PostgreSQL password to connect with                                                                                      |
| `icinga2_feature_idogpsql_database`         | `icinga2`                                             | PostgreSQL database to connect to                                                                                        |
| `icinga2_feature_idogpsql_instance_name`    | `default`                                             | Name for this instance in the DB. Used for HA                                                                            |
| `icinga2_feature_idogpsql_ha`               | `true`                                                | Enable Icinga 2 HA in the database                                                                                       |
| `icinga2_feature_idogpsql_failover_timeout` | `60s`                                                 | HA failover in the database                                                                                              |
| `icinga2_feature_idogpsql_cleanup`          | `{}`                                                  | Items to clean (key) and their maximum age (value)                                                                       |
| `icinga2_feature_mainlog_severity`          | `information`                                         | Minimum log level for messages to be logged                                                                              |
| `icinga2_feature_mainlog_path`              | `/var/log/icinga2/icinga2.log`                        | Path to the mainlog                                                                                                      |
| `icinga2_feature_notification_ha`           | `true`                                                | Whether to enable notification HA                                                                                        |
| `icinga2_feature_syslog_severity`           | `information`                                         | Minimum log level for messages to be logged to syslog                                                                    |
| `icinga2_api_master_users`                  | `{}`                                                  | List of Username-Values dicts of API users configured in this master. See below for possible values                      |
| `icinga2_api_global_users`                  | `{}`                                                  | List of Username-Values dicts of API users configured in the global zone. See below for possible values                  |
| `icinga2_host_dependencies`                 | `{}`                                                  | List of Name-Values dicts of dependencies applied to hosts. See below for possible values                                |
| `icinga2_service_dependencies`              | `{}`                                                  | List of Name-Values dicts of dependencies applied to services. See below for possible values                             |
| `icinga2_host_downtimes`                    | `{}`                                                  | List of Name-Values dicts of scheduled downtimes applied to hosts. See below for possible values                         |
| `icinga2_service_downtimes`                 | `{}`                                                  | List of Name-Values dicts of scheduled downtimes applied to services. See below for possible values                      |
| `icinga2_event_commands`                    | `{}`                                                  | List of Name-Values dicts of event commands. See below for possible values                                               |
| `icinga2_forwarded_vars`                    | `{}`                                                  | List of names of hostvars that are inserted into the custom variables of the corresponding Icinga 2 hosts                |
| `icinga2_noagent_group`                     | `icinga2-noagent`                                     | Name of a group a host has to be in in order to use the `hostalive` check instead of the agent check (see next variable) |
| `icinga2_agent_check`                       | :heavy_check_mark:                                    | Name of the check to perform in order to validate the Icinga 2 client on the machine is alive                            |
| `icinga2_host_groups`                       | `{}`                                                  | Name-Description dict of hostgroups                                                                                      |
| `icinga2_notification_commands`             | `{}`                                                  | List of Name-Values dicts of notification commands. See below for possible values                                        |
| `icinga2_host_notifications`                | `{}`                                                  | List of Name-Values dicts of notifications applied to hosts. See below for possible values                               |
| `icinga2_service_notifications`             | `{}`                                                  | List of Name-Values dicts of notifications applied to services. See below for possible values                            |
| `icinga2_services`                          | `{}`                                                  | List of Name-Values dicts of services applied to hosts. See below for possible values                                    |
| `icinga2_service_groups`                    | `{}`                                                  | Name-Description dict of service groups                                                                                  |
| `icinga2_timeperiods`                       | `{}`                                                  | List of Name-Values dicts of time periods. See below for possible values                                                 |
| `icinga2_users`                             | `{}`                                                  | List of Name-Values dicts of users. See below for possible values                                                        |
| `icinga2_user_groups`                       | `{}`                                                  | Name-Description dict of user groups                                                                                     |
| `icinga2_check_commands`                    | `{}`                                                  | List of Name-Values dicts of check commands. See below for possible values                                               |
| `icinga2_service_max_attempts`              | `3`                                                   | Maximum amount of check attempts on a service. Can be overridden per-service                                             |
| `icinga2_service_volatile`                  | `false`                                               | Whether all services are volatile. Can be overridden per-service                                                         |
| `icinga2_service_check_interval`            | `5m`                                                  | Check interval for services. Can be overridden per-service                                                               |
| `icinga2_service_retry_interval`            | `5m`                                                  | Check interval for services when in a `SOFT` state. Can be overridden per-service                                        |
| `icinga2_service_flapping`                  | `true`                                                | Whether flapping detection is enabled for all services. Can be overridden per-service                                    |
| `icinga2_service_flapping_threshold_high`   | `30.0`                                                | High flapping threshold for all services. Can be overridden per-service                                                  |
| `icinga2_service_flapping_threshold_low`    | `25.0`                                                | Low flapping threshold for all services. Can be overridden per-service                                                   |
| `icinga2_user_default_types`                | All types                                             | Notification types to notify all users about. Can be overridden per-user                                                 |


### API users

| Name            | Default / Mandatory | Description                                                                 |
|:----------------|:-------------------:|:----------------------------------------------------------------------------|
| `password`      |                     | Password of this API user. Either this or `password_hash` is required       |
| `password_hash` |                     | Hashed password of this API user. Either this or `password` is required     |
| `client_cn`     |                     | CN the client is required to have when connecting to the API with this user |
| `permissions`   |                     | List of Icinga 2 API permissions this user holds                            |

### Dependencies

| Name                    | Default / Mandatory | Description                                                                 |
|:------------------------|:-------------------:|:----------------------------------------------------------------------------|
| `parent_host_name`      | :heavy_check_mark:  | Name of the parent host                                                     |
| `parent_service_name`   |                     | Name of the parent service. If omitted, the dependency is made to the  host |
| `disable_checks`        | `false`             | Disable child checks once parent checks fail                                |
| `disable_notifications` | `true`              | Disable child notifications once parent checks fail                         |
| `ignore_soft_states`    | `true`              | Ignore soft states on the parent                                            |
| `period`                |                     | Name of a period where this dependency is valid                             |
| `states`                |                     | List of states that are considered OK                                       |
| `assign`                | :heavy_check_mark:  | List of assign specifications (`assign where` is automatically prepended)   |
| `ignore`                |                     | List of ignore specifications (`ignore where` is automatically prepended)   |

### Scheduled Downtimes

| Name          | Default / Mandatory | Description                                                                                    |
|:--------------|:-------------------:|:-----------------------------------------------------------------------------------------------|
| `author`      | :heavy_check_mark:  | Name of the author of this downtime                                                            |
| `description` | :heavy_check_mark:  | Description of this downtime                                                                   |
| `duration`    |                     | Duration specification of this downtime. If set, converts this downtime to a flexible downtime |
| `ranges`      | :heavy_check_mark:  | Day-Duration dict of downtime ranges                                                           |
| `assign`      | :heavy_check_mark:  | List of assign specifications (`assign where` is automatically prepended)                      |
| `ignore`      |                     | List of ignore specifications (`ignore where` is automatically prepended)                      |

### Commands

| Name      | Default / Mandatory | Description                                                                                                             |
|:----------|:-------------------:|:------------------------------------------------------------------------------------------------------------------------|
| `command` | :heavy_check_mark:  | Command to execute. You need to quote this string yourself, so you can use variables, e.g. `"PluginDir + \"my_check\""` |
| `args`    | `{}`                | Argument-Values dict to pass to the command. See below for valid values                                                 |
| `env`     |                     | Dict to append to the environment of the executed command                                                               |
| `timeout` | `1m`                | Timeout of the command                                                                                                  |
| `vars`    | `{}`                | Variables to pass to the command                                                                                        |

#### Command Arguments

| Name          | Default / Mandatory | Description                                                                         |
|:--------------|:-------------------:|:------------------------------------------------------------------------------------|
| `value`       |                     | Value of this argument                                                              |
| `set_if`      |                     | Set this argument if the condition evaulates to true                                |
| `order`       |                     | Order specification of this argument                                                |
| `description` | :heavy_check_mark:  | Description of this argument                                                        |
| `required`    | `false`             | Whether this argument is required                                                   |
| `skip_key`    | `false`             | Whether to skip the key (name) of this argument when passing it to the command line |
| `repeat_key`  | `true`              | Whether to repeat the key (name) for each occurence of the argument                 |

### Notifications

| Name          | Default / Mandatory                                                | Description                                                               |
|:--------------|:------------------------------------------------------------------:|:--------------------------------------------------------------------------|
| `command`     | :heavy_check_mark:                                                 | Name of the notification command to execute for this notification         |
| `interval`    |                                                                    | Interval in which to renotify                                             |
| `users`       |                                                                    | List of users to notify (either this or `user_groups` is required)        |
| `user_groups` | List of user groups to notify (either this or `users` is required) |
| `zone`        |                                                                    | Zone in which to execute this notification                                |
| `types`       |                                                                    | List of notification types to notify on                                   |
| `states`      |                                                                    | List of states to notify on                                               |
| `period`      |                                                                    | Name of a period in which to notify in                                    |
| `vars`        | `{}`                                                               | Variables to pass to the notification                                     |
| `assign`      | :heavy_check_mark:                                                 | List of assign specifications (`assign where` is automatically prepended) |
| `ignore`      |                                                                    | List of ignore specifications (`ignore where` is automatically prepended) |

### Services

| Name                      | Default / Mandatory                            | Description                                                                                                                                                              |
|:--------------------------|:----------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `for`                     | `false`                                        | Enables the `for (key => value)` assigment                                                                                                                               |
| `for_key`                 | `key`                                          | Key to use for a `for (key => value)` assigment                                                                                                                          |
| `for_value`               | `value`                                        | Key to use for a `for (key => value)` assigment                                                                                                                          |
| `no_name`                 | `false`                                        | Set to true to prevent giving a name to this service (only makes sense in combination with `for`)                                                                        |
| `volatile`                | `false`                                        | Whether this service is volatile                                                                                                                                         |
| `check_command`           | :heavy_check_mark:                             | Command to execute to check this service                                                                                                                                 |
| `max_check_attempts`      | `{{icinga2_service_max_attempts}}`             | Amount of checks before the hard state is set                                                                                                                            |
| `check_period`            |                                                | Period in which to execute the check                                                                                                                                     |
| `check_timeout`           |                                                | Timeout of the check                                                                                                                                                     |
| `check_interval`          | `{{icinga2_service_check_interval}}`           | Interval in which the service is checked                                                                                                                                 |
| `retry_interval`          | `{{icinga2_service_retry_interval}}`           | Interval in which the service is checked when in a `SOFT` state                                                                                                          |
| `event_command`           |                                                | Event command executed for this service                                                                                                                                  |
| `zone`                    |                                                | Zone in which the check is executed                                                                                                                                      |
| `command_endpoint`        | (See next value)                               | Endpoint the check is executed on                                                                                                                                        |
| `remote`                  | `false`                                        | Set to true to execute service checks on this Icinga 2 master instead of the on the client. If false, the service is not applied to hosts in the `icinga2_noagent_group` |
| `flapping`                | `{{icinga2_service_flapping}}`                 | Enable flapping detection for this service                                                                                                                               |
| `flapping_threshold_high` | `{{icinga2_service_flapping_threshold_high}}`  | Flapping upper bound in percent                                                                                                                                          |
| `flapping_threshold_low`  | `{{icinga2_service_flapping_threshold_lower}}` | Flapping lower bound in percent                                                                                                                                          |
| `description`             |                                                | Display name of this service                                                                                                                                             |
| `groups`                  |                                                | List of service groups that are automatically created once mentioned in a service                                                                                        |
| `notes`                   |                                                | Notes about this service                                                                                                                                                 |
| `notes_url`               |                                                | URL for the notes of the service                                                                                                                                         |
| `action_url`              |                                                | URL for actions for the service                                                                                                                                          |
| `icon_image`              |                                                | Icon image for the service                                                                                                                                               |
| `icon_image_alt`          |                                                | Alt text for the icon image of the service                                                                                                                               |
| `vars`                    | `{}`                                           | Custom variables of this service                                                                                                                                         |
| `assign`                  | :heavy_check_mark:                             | List of assign specifications (`assign where` is automatically prepended)                                                                                                |
| `ignore`                  |                                                | List of ignore specifications (`ignore where` is automatically prepended)                                                                                                |

### Time Periods

| Name              | Default / Mandatory | Description                              |
|:------------------|:-------------------:|:-----------------------------------------|
| `description`     |                     | Optional description of this time period |
| `ranges`          | :heavy_check_mark:  | Day-Duration dict of ranges              |
| `includes`        |                     | Name of included time periods            |
| `excludes`        |                     | Name of excluded time periods            |
| `prefer_includes` | `true`              | Whether to prefer includes over excludes |

### Users

| Name                   | Default / Mandatory              | Description                                                                 |
|:-----------------------|:--------------------------------:|:----------------------------------------------------------------------------|
| `name`                 |                                  | Display name of this user                                                   |
| `groups`               |                                  | List of user groups that are automatically created once mentioned in a user |
| `email`                |                                  | Email address of this user                                                  |
| `pager`                |                                  | A pager string for this user                                                |
| `enable_notifications` |                                  | Whether to enable notifications for this user                               |
| `period`               |                                  | Name of a period in which this user is notified in                          |
| `types`                | `{{icinga2_user_default_types}}` | Notifications types to send to this user                                    |
| `states`               |                                  | States on which to notify this user                                         |
| `vars`                 | `{}`                             | Custom variables of this user                                               |

## Example Playbook

```yml
- hosts: icinga
  roles:
    - role: icinga2-master
      icinga2_feature_api_salt: ieChahchaecei8zai1va
      icinga2_feature_idopgsql_ha: false
      icinga2_constants:
        PluginDir: /var/lib/nagios/plugins
      icinga2_users:
        jdoe:
          name: John Doe
          groups: [ admins ]
      icinga2_check_commands:
        dummy:
          command: "PluginDir + \"/check_dummy\""
          args:
            -w:
              description: Foo bar
              value: "$dummy_warning$"
        icinga2_services:
          load:
            command: load
            assign:
              - "true"

        icinga2_agent_check: dummy
```

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Author Information

- [Janne Heß](https://github.com/dasJ)
