uniform sampler2D texture;

void main()
{
    vec2 pos = gl_TexCoord[0].xy;

    gl_FragColor = texture2D(texture, pos);
}
