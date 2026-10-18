shader_type spatial;
render_mode depth_draw_opaque, cull_disabled, diffuse_burley, specular_schlick_ggx;
uniform sampler2D texture_albedo : source_color, filter_nearest;
uniform float wind_speed = 1.5;
uniform float wind_strength = 0.05;
uniform float depth_illusion = 1.2;

void vertex() {
    float sway = sin(TIME * wind_speed + VERTEX.x * 2.0 + VERTEX.z) * wind_strength;
    float height_factor = max(0.0, VERTEX.y * 1.5);
    VERTEX.x += sway * height_factor;
}
void fragment() {
    vec4 albedo_tex = texture(texture_albedo, UV);
    ALBEDO = albedo_tex.rgb;
    ALPHA = albedo_tex.a;
    ALPHA_SCISSOR_THRESHOLD = 0.5;
    vec2 center_uv = UV * 2.0 - 1.0;
    float dist = length(center_uv);
    vec3 pseudo_normal = normalize(vec3(-center_uv.x * depth_illusion, -center_uv.y * depth_illusion, 1.0 - (dist * 0.5)));
    NORMAL_MAP = pseudo_normal * 0.5 + 0.5;
    ROUGHNESS = 0.6;
}