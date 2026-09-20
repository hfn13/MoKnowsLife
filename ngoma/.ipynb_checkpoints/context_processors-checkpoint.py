from .models import PhaseChoice, BlockChoice, WorkoutDrill

def workout_library_context(request):
    phases = PhaseChoice.objects.all()
    blocks = BlockChoice.objects.all()
    drills = WorkoutDrill.objects.all()

    block_by_phase = {
        phase: blocks.filter(phase=phase)
        for phase in phases
    }
    drills_by_block = [
    {
        "block": block,
        "drills": drills.filter(block=block)
    }
    for block in blocks
]

    return {
        "block_by_phase": block_by_phase,
        'drills_by_block' : drills_by_block
    }

