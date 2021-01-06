CREATE (Storm:Storm {title: "Storm"}),(Winter:Winter {title:"Storm"}}),(Canada:Canada {title: "Canada"}),(hot:hot {title: "hot"}),(cold:cold {title: "cold"}),(Flu:Flu {title: "Flu"}),(Snow:Snow {title: "Snow"}),(Indoor:Indoor {title: "Indoor"}),(Safety:Safety {title: "Safety"}),(rain:rain {title: "rain"}),(ice:ice {title: "ice"})

match (n:Storm) set n.type='tropical' return n.type 

match (n:rain) set n.temperature='46f',n.humidity="58 dewpoint 32f",n.pressure='10214mb'  return n.temperature,n.humidity,n.pressure

match (n:Flu) set n.max_body_temperature='38.5 C',n.symptoms="[headache,limb ache,tiredness,dry ough]",n.symptoms_persist='5 days',n.remedy="flu shot"  return n.max_body_temperature,n.symptoms,n.symptoms_persist,n.remedy

match (n:Snow) set n.temperature='-1C',n.Depth="46cm"  return n.temperature,n.Depth

match (n:ice) set n.thick='3.9inch',n.color="grey ice",n.range="4m",n.location="lake"  return n.thick,n.color,n.range,n.location

match (n:Winter) set n.wind_speed='70km/hr',n.month="Jan",n.equipments="shovel",n.cloths="snow jacket"  return n.wind_speed,n.month,n.equipments,n.cloths

match (n:Indoor) set n.temperature='6746',n.humidity="5500"  return n.temperature,n.humidity

MATCH (a:Winter),(b:Snow)
WHERE a.title = 'Winter' AND b.title = 'Snow'
CREATE (a)-[r:ACCOMPANIED_BY]->(b)
RETURN type(r)

MATCH (a:Storm),(b:Safety)
WHERE a.title = 'Storm' AND b.title = 'Safety'
CREATE (a)-[r:INCREASES_CONCERN_OF]->(b)
RETURN type(r)

MATCH (a:rain),(b:Storm)
WHERE a.title = 'rain' AND b.title = 'Storm'
CREATE (a)-[r:RESULTS_IN]->(b)
RETURN type(r)

MATCH (a:Winter),(b:Flu)
WHERE a.title = 'Winter' AND b.title = 'Flu'
CREATE (a)-[r:SEASON_OF]->(b)
RETURN type(r)

MATCH (a:hot),(b:Flu)
WHERE a.title = 'hot' AND b.title = 'Flu'
CREATE (a)-[r:BODY_SYMPTOM_OF]->(b)
RETURN type(r)

MATCH (a:Indoor),(b:Safety)
WHERE a.title = 'Indoor' AND b.title = 'Safety'
CREATE (a)-[r:FIREPLACE]->(b)
RETURN type(r)

MATCH (a:Winter),(b:cold)
WHERE a.title = 'Winter' AND b.title = 'cold'
CREATE (a)-[r:SEASON_OF]->(b)
RETURN type(r)

MATCH (a:cold),(b:rain)
WHERE a.title = 'cold' AND b.title = 'rain'
CREATE (a)-[r:FREEZING]->(b)
RETURN type(r)

MATCH (a:Snow),(b:ice)
WHERE a.title = 'Snow' AND b.title = 'ice'
CREATE (a)-[r:TRANSFORMS_INTO]->(b)
RETURN type(r)
----
MATCH (a:Storm),(b:Canada)
WHERE a.title = 'Storm' AND b.title = 'Canada'
CREATE (a)-[r:STRIKES]->(b)
RETURN type(r)