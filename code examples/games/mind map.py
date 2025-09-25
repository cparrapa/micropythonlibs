import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Central node
G.add_node("Vlny a kmity")

# Main branches
G.add_edge("Vlny a kmity", "Vlny")
G.add_edge("Vlny a kmity", "Kmity")
G.add_edge("Vlny a kmity", "Výučbové stratégie")

# Vlny branch
G.add_edge("Vlny", "Druhy vĺn")
G.add_edge("Vlny", "Charakteristiky vĺn")
G.add_edge("Vlny", "Chovanie vĺn")

# Druhy vĺn
G.add_edge("Druhy vĺn", "Mechanické vlny")
G.add_edge("Druhy vĺn", "Elektromagnetické vlny")

# Mechanické vlny
G.add_edge("Mechanické vlny", "Zvukové vlny")
G.add_edge("Mechanické vlny", "Vodné vlny")
G.add_edge("Mechanické vlny", "Ďalšie mechanické príklady")

# Zvukové vlny
G.add_edge("Zvukové vlny", "Vznik zvuku")
G.add_edge("Zvukové vlny", "Vlastnosti zvuku")
G.add_edge("Zvukové vlny", "Šírenie zvuku")
G.add_edge("Zvukové vlny", "Fenomená zvuku")

# Vznik zvuku
G.add_edge("Vznik zvuku", "Vibrujúce objekty")
G.add_edge("Vznik zvuku", "Ľudský hlas")

# Vlastnosti zvuku
G.add_edge("Vlastnosti zvuku", "Výška tónu - frekvencia")
G.add_edge("Vlastnosti zvuku", "Hlasitosť - amplitúda")
G.add_edge("Vlastnosti zvuku", "Timbre - kvalita tónu")

# Šírenie zvuku
G.add_edge("Šírenie zvuku", "Šírenie v materiáloch")
G.add_edge("Šírenie v materiáloch", "Vzduch")
G.add_edge("Šírenie v materiáloch", "Kvapaliny")
G.add_edge("Šírenie v materiáloch", "Pevné látky")

# Fenomená zvuku
G.add_edge("Fenomená zvuku", "Dopplerov jav")
G.add_edge("Fenomená zvuku", "Rezonancia")

# Elektromagnetické vlny
G.add_edge("Elektromagnetické vlny", "Svetelné vlny")
G.add_edge("Elektromagnetické vlny", "Rádiové vlny")
G.add_edge("Elektromagnetické vlny", "Ďalšie EM vlny")

# Charakteristiky vĺn
G.add_edge("Charakteristiky vĺn", "Frekvencia")
G.add_edge("Charakteristiky vĺn", "Dĺžka vlny")
G.add_edge("Charakteristiky vĺn", "Amplitúda")
G.add_edge("Charakteristiky vĺn", "Rýchlosť vlny = Frekvencia x Dĺžka vlny")
G.add_edge("Charakteristiky vĺn", "Perióda = 1 / Frekvencia")

# Chovanie vĺn
G.add_edge("Chovanie vĺn", "Odraz")
G.add_edge("Chovanie vĺn", "Lom")
G.add_edge("Chovanie vĺn", "Difrakcia")
G.add_edge("Chovanie vĺn", "Interferencia")
G.add_edge("Interferencia", "Konštruktívna")
G.add_edge("Interferencia", "Deštruktívna")

# Kmity branch
G.add_edge("Kmity", "Kmitavý pohyb")
G.add_edge("Kmity", "Periodický pohyb")
G.add_edge("Kmity", "Neperiodický pohyb")
G.add_edge("Kmity", "Jednoduchý harmonický pohyb")
G.add_edge("Jednoduchý harmonický pohyb", "Vlastnosti - opakujúci sa pohyb")
G.add_edge("Jednoduchý harmonický pohyb", "Príklady - kyvadlo, pružina")

G.add_edge("Kmity", "Energia v kmitoch")
G.add_edge("Energia v kmitoch", "Kinetická energia")
G.add_edge("Energia v kmitoch", "Potenciálna energia")
G.add_edge("Energia v kmitoch", "Výměna energie")

G.add_edge("Kmity", "Tlmené a nútené kmity")
G.add_edge("Tlmené a nútené kmity", "Tlmené - trenie")
G.add_edge("Tlmené a nútené kmity", "Nútené - pohyb pod vplyvom sily")

G.add_edge("Kmity", "Stacionárne vlny a rezonancia")
G.add_edge("Stacionárne vlny a rezonancia", "Uzlíky a antuzlíky")
G.add_edge("Stacionárne vlny a rezonancia", "Rezonancia pri vlastnej frekvencii")

# Výučbové stratégie branch
G.add_edge("Výučbové stratégie", "Praktické experimenty")
G.add_edge("Praktické experimenty", "Tladacie vidličky")
G.add_edge("Praktické experimenty", "Vlny na šmútoch")
G.add_edge("Praktické experimenty", "Kyvadlo")

G.add_edge("Výučbové stratégie", "Vizuálne pomôcky")
G.add_edge("Vizuálne pomôcky", "Diagramy vĺn")
G.add_edge("Vizuálne pomôcky", "Simulácie a animácie")

G.add_edge("Výučbové stratégie", "Výučba založená na otázkach")
G.add_edge("Výučba založená na otázkach", "Prieskum študentov")
G.add_edge("Výučba založená na otázkach", "Diskusia v triede")

G.add_edge("Výučbové stratégie", "Medzidisciplinárne väzby")
G.add_edge("Medzidisciplinárne väzby", "Grafy a vzorce")
G.add_edge("Medzidisciplinárne väzby", "Vzor vĺn v umení")
G.add_edge("Medzidisciplinárne väzby", "Zvuková technika a reproduktory")

# Generate layout for a visually pleasing view (using spring layout)
plt.figure(figsize=(16, 12))
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the nodes and edges
nx.draw(G, pos,
        with_labels=True,
        node_size=3000,
        node_color="#AED6F1",
        font_size=9,
        font_weight="bold",
        arrows=True,
        arrowstyle='->',
        arrowsize=10)

plt.title("Mind Map: Vlny a kmity", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()
