{% set spline=spline or 'cubic_spline' %}
{% set radius=radius or 1.0 %}

global_settings {
  assumed_gamma 1
}
    
{% for line, colour in lines %}
#declare line{{ loop.index }} = sphere_sweep {
  {{ spline }}
  {{ line|length }}
  {% for row in line %}<{{ row[0] }},{{ row[1] }},{{ row[2] }}> {{ radius }}
  {% endfor %}
}
{% endfor %}

#declare line_union = union {
  {% for line, colour in lines %}
  object {
    line{{ loop.index }}
    texture {
      pigment {
        color rgb <{{ colour[0] }},{{ colour[1] }},{{ colour[2] }}>
      }
      finish {
        phong 0.3
        metallic
      }
    }
  }
  {% endfor %}
}

object {
  line_union
}

background { 
  color rgb <1, 1, 1>
}

light_source {
  <125, 125, 250>
  rgb <1,1,1>
  spotlight
  area_light <1,0,0>, <0,0,1>, 2, 2
  adaptive 1
  jitter
  falloff 50
  tightness 10
  point_at <125, 125, 125>
  
}

camera {
   perspective
  location <125,125,500>
  //  right <1.776, 0, 0>
  //  up <0, 0, 1>
  // sky <0,0,1>
  look_at <125, 125, 125>
}