shader_type spatial;
render_mode depth_draw_opaque, cull_disabled;
uniform sampler2D texture_albedo : source_color, filter_nearest;
void fragment() {
    vec4 tex = texture(texture_albedo, UV);
    ALBEDO = tex.rgb;
    ALPHA = tex.a;
    ALPHA_SCISSOR_THRESHOLD = 0.5;
}