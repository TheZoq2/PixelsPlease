uniform sampler2D texture;

void main()
{
    vec2 pos = gl_TexCoord[0].xy;

    vec4 color = texture2D(texture, pos);
    color.a = color.a * (1. - color.r);
    gl_FragColor = color;
}
