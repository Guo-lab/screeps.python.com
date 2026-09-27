from defs import *

__pragma__("noalias", "name")
__pragma__("noalias", "undefined")
__pragma__("noalias", "Infinity")
__pragma__("noalias", "keys")
__pragma__("noalias", "get")
__pragma__("noalias", "set")
__pragma__("noalias", "type")
__pragma__("noalias", "update")


def run_harvester(creep):
    """Harvest energy, refill Spawn/Extensions, then upgrade the Controller."""

    energy = creep.store.getUsedCapacity(RESOURCE_ENERGY)
    free_capacity = creep.store.getFreeCapacity(RESOURCE_ENERGY)

    if creep.memory.filling and free_capacity == 0:
        creep.memory.filling = False
        creep.say("deliver")
    elif not creep.memory.filling and energy == 0:
        creep.memory.filling = True
        creep.say("harvest")

    if creep.memory.filling:
        source = creep.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        if not source:
            return

        result = creep.harvest(source)
        if result == ERR_NOT_IN_RANGE:
            creep.moveTo(source, {"visualizePathStyle": {"stroke": "#ffaa00"}})
        elif result != OK:
            print("[{}] harvest failed: {}".format(creep.name, result))
        return

    target = creep.pos.findClosestByPath(
        FIND_MY_STRUCTURES,
        {
            "filter": lambda structure: (
                structure.structureType == STRUCTURE_SPAWN
                or structure.structureType == STRUCTURE_EXTENSION
            )
            and structure.store.getFreeCapacity(RESOURCE_ENERGY) > 0
        },
    )

    if target:
        result = creep.transfer(target, RESOURCE_ENERGY)
        if result == ERR_NOT_IN_RANGE:
            creep.moveTo(target, {"visualizePathStyle": {"stroke": "#ffffff"}})
        elif result != OK:
            print("[{}] transfer failed: {}".format(creep.name, result))
        return

    controller = creep.room.controller
    if controller:
        result = creep.upgradeController(controller)
        if result == ERR_NOT_IN_RANGE:
            creep.moveTo(controller, {"visualizePathStyle": {"stroke": "#ffffff"}})
        elif result != OK:
            print("[{}] upgrade failed: {}".format(creep.name, result))
