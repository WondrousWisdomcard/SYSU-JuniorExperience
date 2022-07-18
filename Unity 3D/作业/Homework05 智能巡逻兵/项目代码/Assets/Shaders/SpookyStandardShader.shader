Shader "Custom/SpookyStandardShader"
{
	Properties{
		_Color("Color", Color) = (1,1,1,1)
		_MainTex("Albedo (RGB)", 2D) = "white" {}
		_Glossiness("Smoothness", Range(0,1)) = 0.5
		_Metallic("Metallic", Range(0,1)) = 0.0
		_BumpScale("Scale", Float) = 1.0
		_BumpMap("Normal Map", 2D) = "bump" {}
		_RimColor("Rim Color", Color) = (1,1,1,1)
		_RimMask("Rim Mask", 2D) = "white" {}
		_RimPower("Rim Power", Range(0.01,10.0)) = 3
		_RimBias("Rim Bias", Range(0.1,1.0)) = 0.5
		_EmissiveMap("Emission", 2D) = "black" {}
		[HDR]_EmissiveColor("Emission Color", Color) = (0,0,0,0)
		_DetailMask("Detail Mask(A)",2D) = "gray"{}
		_Detail("Detail (RGB)", 2D) = "gray" {}
	}
		SubShader{
		Tags{ "RenderType" = "Transparent" "Queue"="Transparent+1" }

        Pass
        {
            ZWrite On
            ColorMask 0
        }

		Blend SrcAlpha OneMinusSrcAlpha
		ColorMask RGBA
		ZWrite On
		LOD 200

		CGPROGRAM
#pragma surface surf Standard fullforwardshadows alpha
#pragma target 3.0

		sampler2D _MainTex;
		sampler2D _BumpMap;
		sampler2D _RimMask;
		sampler2D _Detail;
		sampler2D _DetailMask;
		sampler2D _EmissiveMap;

	struct Input {
		float2 uv_MainTex;
		fixed3 viewDir;
		float2 uv_Detail;
		float2 uv_DetailMask;
	};
	half _Glossiness;
	half _Metallic;
	fixed4 _Color;
	fixed4 _RimColor;
	fixed _RimPower;
	fixed _RimBias;
	fixed Alpha;
	float4 _EmissiveColor;
	
	void surf(Input IN, inout SurfaceOutputStandard o) 
	{
		fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color;
		fixed3 normal = UnpackScaleNormal(tex2D(_BumpMap, IN.uv_MainTex),1);
		fixed4 rimMask = tex2D(_RimMask, IN.uv_MainTex);
		fixed4 mask = tex2D(_DetailMask, IN.uv_DetailMask);
		fixed4 detail = tex2D(_Detail,IN.uv_Detail);
		c.rgb *= detail.rgb * 2;
		o.Albedo = c.rgb;
		o.Normal = normal;
		o.Metallic = _Metallic;
		o.Smoothness = _Glossiness;
		o.Alpha = c.a;

		half4 emission = tex2D(_EmissiveMap, IN.uv_MainTex) * _EmissiveColor;
		o.Emission = emission.rgb;

		fixed3 view = normalize(IN.viewDir);
		fixed3 nml = o.Normal;
		fixed VdN = dot(view, nml);
		fixed rim = _RimBias - saturate(VdN);
		o.Emission = (smoothstep(1 - _RimColor.rgb, _RimBias, (rim - rimMask)) * _RimPower) + emission;

	}
	ENDCG
	}
		FallBack "Diffuse"
}
