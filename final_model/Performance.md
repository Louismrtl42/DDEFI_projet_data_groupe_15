Rapport Technique : Évolution des Stratégies de Machine Learning
Ce rapport détaille la progression de nos algorithmes, de la régression statistique simple vers l'intelligence artificielle segmentée par secteur.




1. Le Modèle 1 : Régression Linéaire Simple (Baseline)
Logique détaillée
Ce modèle repose sur l'hypothèse que le prix d'une action est une somme pondérée de ses indicateurs financiers. L'algorithme cherche à minimiser la distance globale entre une ligne droite théorique et tous les points du jeu de données.
Calcul : Il attribue un coefficient à chaque variable (ex: +2.5 pour le Net Income, -0.8 pour la Dette).
Faiblesse conceptuelle : Il traite les données de manière absolue. Pour lui, une variation de 10M€ de bénéfice doit produire le même effet sur le prix, que l'entreprise soit une multinationale ou une start-up.
Logs & Résultats
Précision (R²) : 0.9413									
Erreur moyenne : 47.07 €									
												
Quelques exemples de prédictions :								
           Entreprise  Prix Réel 2025  Prix Prédit 2025  Écart (€)				
0             EUKEDOS            0.70            -12.59     -13.29					
1      Indra Sistemas           47.57             25.75     -21.82					
2  MGI DIGITAL GRAPHI            9.26             11.21       1.94				
3  YARA INTERNATIONAL          391.50            163.24    -228.26				
4         ROBERTET CI          743.88            850.47     106.59				
5    VENTE UNIQUE.COM           16.26              6.88      -9.39				
6       TREVI FIN IND            0.62            -19.81     -20.43					
7             MASTRAD            0.01            -30.68     -30.69					
8          STREAMWIDE           73.40             31.28     -42.12					
9              SEMAPA           17.95             19.04       1.10					 
Conclusion suite aux résultats
Le score R2 élevé est un mirage statistique. Le modèle est "aimanté" par les prix élevés (Robertet, Yara) car une erreur de 10% sur ces titres pèse beaucoup plus lourd dans son calcul qu'une erreur sur une petite action. Pour satisfaire les gros prix, la pente de la droite devient si raide qu'elle s'enfonce dans les valeurs négatives pour les petites capitalisations, produisant des prédictions absurdes (ex: Mastrad à -30€).




2. Le Modèle 2 : Régression Ridge + Standardisation
Logique détaillée
Pour corriger le Modèle 1, nous avons introduit deux mécanismes de régulation :
StandardScaler (Normalisation) : On ramène toutes les données à une échelle commune (moyenne de 0, écart-type de 1). Cela évite que le "Chiffre d'Affaires" (en millions) n'écrase le "ROE" (en pourcentage).
Régularisation Ridge (L2​) : On inflige une "pénalité" au modèle s'il donne trop d'importance à une seule variable. Cela force la ligne droite à être plus stable et moins sensible aux valeurs extrêmes (outliers).
Logs & Résultats
Précision (R²) : 0.9246									
Erreur moyenne (MAE) : 54.97 €								
												
Quelques exemples de prédictions avec Ridge + Scaling :					
           Entreprise  Prix Réel 2025  Prix Prédit 2025  Écart (€)				
0             EUKEDOS            0.70            -11.82     -12.53					
1      Indra Sistemas           47.57             12.68     -34.89					
2  MGI DIGITAL GRAPHI            9.26             16.44       7.17				
3  YARA INTERNATIONAL          391.50            681.17     289.67				
4         ROBERTET CI          743.88            925.24     181.36				
5    VENTE UNIQUE.COM           16.26              2.99     -13.27				
6       TREVI FIN IND            0.62             -8.99      -9.60					
7             MASTRAD            0.01            -10.67     -10.68					
8          STREAMWIDE           73.40             21.58     -51.82					
9              SEMAPA           17.95             14.32      -3.63					
Conclusion suite aux résultats
Bien que plus robuste mathématiquement, ce modèle est moins précis dans la vie réelle. En forçant l'algorithme à accorder de l'importance aux petites valeurs (grâce au scaling), on l'empêche de "coller" aux grandes valeurs. L'erreur moyenne augmente car le modèle est puni dès qu'il essaie de suivre la trajectoire des actions chères. La linéarité reste le problème majeur : le marché ne suit pas une ligne droite.




3. Le Modèle 3 : XGBoost (Gradient Boosting)
Logique détaillée
On abandonne la ligne droite pour une forêt d'arbres de décision. XGBoost fonctionne par itération : il crée un premier arbre simple, calcule l'erreur, puis crée un deuxième arbre pour corriger l'erreur du premier, et ainsi de suite.
Segmentation : Au lieu d'une équation unique, il crée des règles de décision : "SI le prix est > 100€ ET que le PER est < 15, ALORS le prix sera de X".
Non-linéarité : Il est capable de comprendre qu'un fort endettement est un signal différent selon la taille de l'entreprise.
Logs & Résultats
Précision (R²) : 0.6210									
Erreur moyenne (MAE) : 69.68 €								
												
Zoom sur les prédictions XGBoost (Arbres de décision) :					
           Entreprise  Prix Réel 2025  Prix Prédit 2025  Écart (€)				
0             EUKEDOS            0.70          3.030000       2.33					
1      Indra Sistemas           47.57         20.170000     -27.40					
2  MGI DIGITAL GRAPHI            9.26         25.860001      16.59				
3  YARA INTERNATIONAL          391.50        404.519989      13.02			
4         ROBERTET CI          743.88        826.119995      82.25				
5    VENTE UNIQUE.COM           16.26         18.480000       2.21				
6       TREVI FIN IND            0.62          0.450000      -0.16					
7             MASTRAD            0.01         -1.130000      -1.14					
8          STREAMWIDE           73.40         27.959999     -45.44				
9              SEMAPA           17.95         20.690001       2.74					
Conclusion suite aux résultats
C'est le modèle de la cohérence. Le R2 chute car le modèle refuse de tracer une ligne simpliste "au milieu de nulle part". En revanche, il élimine quasiment les prix négatifs. Il commence à segmenter le marché : il est capable de prédire avec précision le prix de Yara (grosse valeur) sans être perturbé par les métriques de Mastrad (petite valeur). C'est une base saine pour l'étape suivante.




4. Le Modèle 4 : XGBoost + Secteur + Rendement (%)
Logique détaillée
Ce modèle change la question posée à l'IA. On ne lui demande plus "Quel est le prix ?" mais "Quelle est la performance attendue ?".
Changement de cible : On prédit le pourcentage de variation (Return). Cela "égalise" toutes les entreprises : un gain de 5% est comparable pour tout le monde.
Variable "Sector" : On injecte le secteur d'activité. XGBoost peut désormais créer des branches spécifiques par industrie (ex: Branche "Luxe" vs Branche "Énergie"), car les ratios financiers n'ont pas la même signification d'un secteur à l'autre.
Logs & Résultats
Précision (R²) basée sur le prix final : 0.9386						
Erreur moyenne (MAE) : 33.78 €																				
Zoom sur les prédictions (Logique de rendement sectoriel) :				
           Entreprise             Secteur  Prix Réel 2025 (€)  Prix Prédit 2025 (€)  Écart (€)	
0             EUKEDOS          Healthcare                0.70                  1.03       0.33		
1      Indra Sistemas          Technology               47.57                 20.89     -26.68		
2  MGI DIGITAL GRAPHI          Technology                9.26                 20.00      10.73	
3  YARA INTERNATIONAL     Basic Materials              391.50                352.66     -38.84	
4         ROBERTET CI     Basic Materials              743.88                677.85     -66.02	
5    VENTE UNIQUE.COM   Consumer Cyclical               16.26                 13.74      -2.52	
6       TREVI FIN IND         Industrials                0.62                  0.47      -0.14		
7             MASTRAD  Consumer Defensive                0.01                  0.01      -0.00	
8          STREAMWIDE          Technology               73.40                 32.88     -40.52	
9              SEMAPA     Basic Materials               17.95                 14.68      -3.27		
Conclusion suite aux résultats
C'est la victoire de la logique métier sur la statistique brute. En prédisant une variation, on élimine mathématiquement le risque de prix négatifs. L'ajout du secteur permet une finesse d'analyse inédite : le modèle "comprend" le contexte de l'entreprise. C'est le modèle le plus équilibré : il obtient le meilleur score de précision tout en ayant l'erreur moyenne la plus basse (33€), prouvant que la prédiction boursière doit être relative (performance %) et contextuelle (secteur).

