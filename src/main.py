import harvester

from defs import *

__pragma__("noalias", "name")
__pragma__("noalias", "undefined")
__pragma__("noalias", "Infinity")
__pragma__("noalias", "keys")
__pragma__("noalias", "get")
__pragma__("noalias", "set")
__pragma__("noalias", "type")
__pragma__("noalias", "update")

HARVESTERS_PER_ROOM = 4
HARVESTER_BODY = [WORK, CARRY, MOVE]


def run_creeps():
    """Assign legacy creeps safely and dispatch creeps by role."""

    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]

        # Creeps created by the old starter had no role. Only migrate workers
        # that can both harvest and carry; creeps with an existing role keep it.
        if not creep.memory.role:
            if (
                creep.getActiveBodyparts(WORK) > 0
                and creep.getActiveBodyparts(CARRY) > 0
            ):
                creep.memory.role = "harvester"
                creep.memory.filling = True

        if creep.memory.role == "harvester":
            if creep.getActiveBodyparts(WORK) > 0:
                harvester.run_harvester(creep)


def count_room_harvesters(room_name):
    count = 0
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if (
            creep.memory.role == "harvester"
            and creep.pos.roomName == room_name
        ):
            count += 1
    return count


def run_spawns():
    """Maintain a small harvester workforce in every spawn room."""

    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if spawn.spawning:
            continue

        harvester_count = count_room_harvesters(spawn.pos.roomName)
        if harvester_count >= HARVESTERS_PER_ROOM:
            continue

        creep_name = "Harvester-{}-{}".format(spawn.name, Game.time)
        result = spawn.spawnCreep(
            HARVESTER_BODY,
            creep_name,
            {"memory": {"role": "harvester", "filling": True}},
        )

        # ERR_NOT_ENOUGH_ENERGY is expected while the room is refilling.
        if result != OK and result != ERR_NOT_ENOUGH_ENERGY and result != ERR_BUSY:
            print("[{}] spawnCreep failed: {}".format(spawn.name, result))


def main():
    run_creeps()
    run_spawns()


module.exports.loop = main
