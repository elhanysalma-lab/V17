extends SceneTree
func _initialize():
    print("=== [Noury V17] Godot Cinematic Engine ===")
    var root_node = Node3D.new()
    root_node.name = "ProductionRoot"
    root.add_child(root_node)
    
    var world_env = WorldEnvironment.new()
    var env = Environment.new()
    env.sdfgi_enabled = true
    env.volumetric_fog_enabled = true
    env.volumetric_fog_density = 0.04
    env.volumetric_fog_albedo = Color(0.8, 0.9, 1.0)
    env.dof_blur_far_enabled = true
    env.dof_blur_far_distance = 5.0
    env.tonemap_mode = Environment.TONE_MAPPER_ACES
    world_env.environment = env
    root_node.add_child(world_env)
    
    print("✓ Moteur Godot 4.x prêt avec SDFGI et Volumetric Fog.")
    quit()
