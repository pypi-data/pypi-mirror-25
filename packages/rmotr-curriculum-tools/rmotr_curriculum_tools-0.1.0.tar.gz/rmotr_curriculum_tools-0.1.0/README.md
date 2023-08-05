<a href="https://travis-ci.org/rmotr/rmotr-curriculum-tools" target="_blank"><img src="https://travis-ci.org/rmotr/rmotr-curriculum-tools.svg"></a>

# rmotr.com curriculum tools

Currently available commands:

```bash
# Create unit in a given course. Order is optional, will be
# appended at the end by default
$ rmotr_curriculum_tools create_unit PATH_TO_COURSE UNIT_NAME -o UNIT_ORDER

# Create lesson in a given unit. Order is optional, will be
# appended at the end by default
$ rmotr_curriculum_tools create_lesson PATH_TO_UNIT LESSON_NAME -t lesson-type -o LESSON_ORDER

# Remove a specific unit by providing its path
$ rmotr_curriculum_tools remove_unit PATH_TO_UNIT

# Remove a specific lesson by providing its path
$ rmotr_curriculum_tools remove_lesson PATH_TO_LESSON
```

### Installation

`$ pip install rmotr_curriculum_tools`

### Testing

```bash
$ make test
```
