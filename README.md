TacticalDays

Classes d'unité:

- Inf    #Infanterie
- Inf_LD #Longue Distance
- VL     #Véhicule_Leger
- PL     #Poid_Lourd
- Tr     #Transport


json.route
{
"ID" : 10000,

"dep.Inf" : 1,      # dep difficulté de deplacement
"couv.Inf" : 1,     # couv pour point de couverture
"fog.Inf" : 1,      # fog visible dans brouillard de guerre

"dep.Inf_LD" : 1,   # 1 pour le nombre de pas
"couv.Inf_LD" : 1,  # 1 pour la puissance de protection
"fog.Inf_LD" : 1,   # 1 pour visible, 2 pour invisible

"dep.VL" : 1,
"couv.VL" : 1,
"fog.VL" : 1,

"dep.PL" : 1,
"couv.PL" : 1,
"fog.PL" : 1,

"dep.Tr" : 1,
"couv.VL" : 1,
"fog.VL" : 1,

}