from scripts.utility.logger import Logger
from dataclasses import dataclass
from typing import Optional

## This class has purposely been built in a manner that allows the programmer to add tags to objects using the Tag
## Handler. Your object, such as a player, stores an instance of a Tag Handler that manages what tags the player holds.
## New tags are added globally meaning any data stored alongside that tag can be stored once in a Tag dataclass.

## Yes this may seem overengineered for now, but if I wanted the tags to store large amount of data, or I want to
## strictly manage what tags exist, separate from assignment, this seems like a good way of handling it. :P


@dataclass
class Tag:
        name: str
        description: Optional[str] = None



class TagHandler:

    __NEW_TAG_ADDED = "New Tag '{tag_name}' added to global tags dict."
    __TAG_ALREADY_EXISTS = "Tag '{tag_name}' already exists in global tags dict."
    __TAG_DOES_NOT_EXIST = "Tag '{tag_name}' does not exist in global tags dict."
    __TAG_REMOVED = "Tag '{tag_name}' removed from global tags dict."

    __TAG_ASSIGNED = "Tag '{tag_name}' assigned to {assignee_name}."
    __TAG_UNASSIGNED = "Tag '{tag_name}' unassigned to {assignee_name}."
    __TAG_ALREADY_ASSIGNED = "Tag '{tag_name}' already assigned to {assignee_name}."
    __TAG_NOT_ASSIGNED = "Tag '{tag_name}' not assigned to {assignee_name}."

    __global_tags: dict[str, Tag] = {}



    def __init__(self):
        self.__tags: set[str] = set()



    ## These methods manipulate the global tags store statically, they do not assign tags to individual instances.

    @staticmethod
    def add_tag(tag: Tag) -> bool:

        if not TagHandler.is_tag(tag.name):
            TagHandler.__global_tags[tag.name] = tag
            Logger.log_info(TagHandler.__NEW_TAG_ADDED.format(tag_name=tag.name))
            return True

        else:
            Logger.log_warning(TagHandler.__TAG_ALREADY_EXISTS.format(tag_name=tag.name))
            return False

    @staticmethod
    def is_tag(name: str) -> bool:
        return name in TagHandler.__global_tags

    @staticmethod
    def get_tag(name: str) -> Tag | None:

        if not Logger.raise_key_error(TagHandler.__global_tags, name, TagHandler.__TAG_DOES_NOT_EXIST.format(tag_name=name)):
            return TagHandler.__global_tags[name]

    @staticmethod
    def remove_tag(name: str) -> bool:

        if not Logger.raise_key_error(TagHandler.__global_tags, name, TagHandler.__TAG_DOES_NOT_EXIST.format(tag_name=name), False):
            del TagHandler.__global_tags[name]
            Logger.log_info(TagHandler.__TAG_REMOVED.format(tag_name=name))
            return True

        return False



    ## These methods are for modifying assignments of tags for a give instance of an object. Tags must first exist
    ## globally before being assigned to individuals.

    def assign_tag(self, name: str, assignee: any) -> bool:

        if TagHandler.is_tag(name):
            if not self.is_tag_assigned(name):
                self.__tags.add(name)
                Logger.log_info(TagHandler.__TAG_ASSIGNED.format(tag_name=name, assignee_name=assignee))
                return True

            else:
                Logger.log_warning(TagHandler.__TAG_ALREADY_ASSIGNED.format(tag_name=name, assignee_name=assignee))

        else:
            Logger.log_warning(TagHandler.__TAG_DOES_NOT_EXIST.format(tag_name=name))

        return False


    def is_tag_assigned(self, name: str) -> bool:
        return name in self.__tags


    def unassign_tag(self, name: str, assignee: any) -> bool:
        if self.is_tag_assigned(name):
            self.__tags.remove(name)
            Logger.log_info(TagHandler.__TAG_UNASSIGNED.format(tag_name=name, assignee_name=assignee))
            return True

        else:
            Logger.log_warning(TagHandler.__TAG_NOT_ASSIGNED.format(tag_name=name, assignee_name=assignee))
            return False

