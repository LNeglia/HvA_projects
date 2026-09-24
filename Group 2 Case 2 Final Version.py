# De onderzoeksvraag van onze groep is: "Hoe presteren verschillende genres op Netflix qua IMDb-beoordelingen, en hoe verschilt deze waarde tussen films en tv-series?"

# %%


import kagglehub
import pandas as pd
import os
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
# Button to rerun the file


st.title("Group 2: Case 2 - Netflix IMDb vergelijking Dashboard")


st.header("Deel 1: Inleiding")
with st.expander("Doel een Onderzoeksvraag van taak", expanded=True):
    st.markdown("""
    In dit dashboard onderzoeken we hoe verschillende genres op Netflix
    presteren op basis van hun IMDb-beoordelingen en vergelijken we hierbij
    films met tv-series.

    **Onderzoeksvraag:**  
    *Hoe presteren verschillende genres op Netflix qua IMDb-beoordelingen,
    en hoe verschilt deze waarde tussen films en tv-series?*

    Hiervoor werden twee datasets gebruikt. De eerste was een Netflix-dataset met uploadgegevens zoals titels, productie- en uploaddata en genres.
    De tweede was een dataset met Netflix-titels, met het type serie en de bijbehorende IMDb-score.
    """)

# Function to import, read, output and cache a dataframe from a csv file imported via Kaggle
@st.cache_data
def import_kaggle_data_source(source):
    path = kagglehub.dataset_download(source)
    file_name = os.listdir(path)[0]
    df = pd.read_csv(path + "/" + file_name)
    return df
    
# Dataframe of dataset 1: Netflix shows/movies registry
netflix = import_kaggle_data_source("shivamb/netflix-shows")

# Dataframe of dataset 2: Netflix shows/movies IMDb scores
imdb = import_kaggle_data_source("thedevastator/netflix-imdb-scores")


# Nu beide datasets zijn geïmporteerd, is het volgende doel ze op te schonen. Om dit te doen, printen we de namen van de kolommen van beide datasets af, zodat we kunnen zien wat we niet hoeven te bewaren. De kolommen die we voor elke dataset hebben gekozen, zijn de titel, het jaar van uitgave, het mediatype en de relevante kolom die we willen vergelijken. Voor de Netflix-database zijn dat de genres van de items. Voor de IMDb-database zijn dat de beoordelingen voor elk item.
# De volgende stap voor elk dataframe is het plannen van het samenvoegen van de dataframes. Omdat er al eerder media met dezelfde titel zijn geweest, houden we daar rekening mee door de kolommen met titel en jaar samen te voegen tot een nieuwe kolom, "title_release_year". Zodra deze nieuwe kolom is aangemaakt, plaatsen we deze vooraan in het dataframe en verwijderen we de oorspronkelijke kolommen met titel en jaar. Dit resulteert in een overzichtelijke en duidelijke opmaak van "title (release_year)" voor elk item.
# %%
with st.expander("Eerste stap van datamanipulatie", expanded=True):
    st.markdown("""Na het importeren van beide datasets en het cachen van de gegevens met behulp van `@st.cachedata`in een
    functie die wordt gebruikt om de `.csv`-bestanden te importeren en te lezen, printen we de kolommen voor elke
    optie af om te bepalen welke relevant zijn om te behouden.""")

    temp_list_netflix = list(netflix.columns)
    temp_list_imdb = list(imdb.columns)



    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Netflix kolom lijst")
        st.write(temp_list_netflix)

    with col2:
        st.subheader("IMDb kolom lijst")
        st.write(temp_list_imdb)



# %%


netflix = netflix[['title', 'release_year', 'listed_in', 'type']]
netflix["title_release_year"] = netflix["title"] + " (" + netflix["release_year"].astype(str) + ")"
netflix = netflix.drop(columns = ["title", "release_year"])
netflix.insert(0, "title_release_year", netflix.pop("title_release_year"))



# %%


# %%


imdb = imdb[['title', 'release_year', 'type', 'imdb_score']]
imdb["title_release_year"] = imdb["title"] + " (" + imdb["release_year"].astype(str) + ")"
imdb = imdb.drop(columns = ["title", "release_year"])
imdb.insert(0, "title_release_year", imdb.pop("title_release_year"))

st.header("Deel 2: Datasets filteren")

with st.expander("Welke kolommen te kiezen?", expanded=True):
    st.markdown("""
    De kolommen die we voor elke dataset hebben gekozen, zijn "`title`", "`release_year`", "`type`" en de relevante kolom die we willen vergelijken.
    Voor de Netflix-database zijn dit de genres van de items, dus "`listed_in`".
    Voor de IMDb-database zijn dit de beoordelingen voor elk item, dus "`imdb_score`".
    """)

with st.expander("Welke kolommen te kiezen?", expanded=True):
    st.write("""De volgende stap voor elk dataframe is het samenvoegen ervan. Omdat er al eerder media met dezelfde titel zijn geweest, houden we hier rekening mee door de kolommen "`title`" en "`release_year`" samen te voegen tot een nieuwe kolom, 'titel_uitgavejaar'.
        Zodra deze nieuwe kolom is aangemaakt, plaatsen we deze vooraan in het dataframe en verwijderen we de oorspronkelijke kolommen "`title`" en "`release_year`". Dit resulteert in een overzichtelijke lay-out van "`title_release_year`" voor elk item.
        """)
    st.write("""Vervolgens ziet de `.head()` van elk dataframe er als volgt uit:""")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Netflix lijst")
        st.write(netflix.head())

    with col2:
        st.subheader("IMDb lijst")
        st.write(imdb.head())




# Om een tweede kolom toe te voegen voor het samenvoegen, maken we de kolom 'type' van Netflix exact hetzelfde als in de IMDb-database. Op deze manier hebben we bij het samenvoegen van de twee dataframes niet alleen de titel en het jaar als kolom, maar ook het media-inhoudstype als secundaire overeenkomstvoorwaarde. Dit is om rekening te houden met items met dezelfde titel en releasedatum, maar waarbij het ene een film is en het andere een serie, zoals Manhunt (2017).

# %%
with st.expander("Mogelijke uitzonderingen buiten beschouwing laten", expanded=True):
    st.write("""We moeten er echter ook rekening mee houden dat er films en tv-series met dezelfde naam en hetzelfde jaar kunnen zijn,
    maar dat het om verschillende mediatypen gaat. Een voorbeeld van dit soort overlapping staat binnen het IMDB lijst, namens Manhunt (2017):""")

    st.write(imdb.loc[imdb["title_release_year"] == "Manhunt (2017)"])

    st.write("""Daarom gebruiken we ook de kolom 'type' voor de samenvoeging, maar de manier waarop 'type' in elk dataframe wordt weergegeven, verschilt.
    We passen de notatie van de "Netflix"-database daarom aan de notatie van "IMDb" aan.""")



# Om de IMDb set te matchen omdat we op "title_release_year" en "type" een merge maken.
netflix["type"] = netflix["type"].replace({
    "TV Show": "SHOW",
    "Movie": "MOVIE"})


# %%


# Merging the dataframes together
merged = pd.merge(netflix, imdb, on = ["title_release_year", "type"], how = "inner")



with st.expander("Na `.merge()` dataframe status en wat volgt", expanded=True):
    st.write("Na de samenvoeging zouden we een overzichtelijk dataframe moeten hebben dat alles combineert, precies zoals gepland:")
    st.write(merged.head())
    st.write("Nu het samengevoegde dataframe klaar is om mee te werken, controleren we op eventuele NA-waarden om deze te verwijderen.")
    st.write("Aantaal NA waardes: ", merged.isna().sum())


# %%
genres = merged["listed_in"].str.split(", ").explode().unique()
gekozen_genres = ["Action & Adventure", "Comedies", "Dramas", "Horror Movies", "Sci-Fi & Fantasy", "Thrillers",
                  "TV Action & Adventure", "TV Comedies", "TV Dramas", "TV Horror", "TV Sci-Fi & Fantasy", "TV Thrillers"]

with st.expander("Kiezen van genres", expanded=True):
    st.write("""Nu we hebben vastgesteld dat de samenvoeging geen NA-waarden bevat, kunnen we verdergaan met de volgende stap: het bekijken van elk genre in de kolom "listed_in", zodat we genres die we niet belangrijk vinden eruit kunnen filteren.""")
    st.write(genres)
    st.write("""Zoals te zien is, heeft elk belangrijk genre een bijbehorende tv- en filmnaam. We filteren de resultaten dus op de genres die we willen en maken daar een lijst van. Vervolgens kunnen we een gefilterde dataset maken op basis van alleen de items die een van de gewenste genres bevatten.""")
    st.write("""Dat geeft ons als volgt: """, gekozen_genres)


# %%

with st.expander("Dataset filteren en verenigen", expanded=True):
    st.write("""Nadat we onze dataset hebben gefilterd met behulp van die lijst, gaan we verder met de volgende stap. Omdat we genres willen vergelijken,
    maar onze filterlijst voor elk genre een tv- en een filmvariant bevat, lossen we dit probleem op door het voorvoegsel "tv" en het achtervoegsel "films" van elk genre te verwijderen.
    Dit voorkomt problemen waarbij bijvoorbeeld drama en tv-drama anders worden geteld.""")


merged_filtered = merged[merged["listed_in"].str.split(", ").apply(lambda genres: any(genre in gekozen_genres for genre in genres))]



# Nu het filteren is voltooid, kunnen we eindelijk de verdeling in een grafiek weergeven. Omdat de namen voor films en tv-series binnen elk genre echter nog steeds enigszins verschillen, zou de grafiek de film- en tv-versies als aparte genres behandelen. Om dit op te lossen, maken we een definitief dataframe, genre_data, waarbij we het voorvoegsel "TV" en het achtervoegsel "Movies" verwijderen uit elke vermelding in "listed_in", zodat de genres overeenkomen in hoofdletters en kleine letters. Hierdoor kan elke rij een genre zijn, terwijl de kolom het mediatype weergeeft.

# %%

genre_data = merged_filtered.copy()

genre_data["genre"] = genre_data["listed_in"].str.split(", ")
genre_data = genre_data.explode("genre")

genre_data = genre_data[genre_data["genre"].isin(gekozen_genres)]
genre_data.insert(3, "genre", genre_data.pop("genre"))

# Remove "TV " prefix from TV genres
genre_data["genre"] = genre_data["genre"].str.replace("TV ", "")
genre_data["genre"] = genre_data["genre"].str.replace(" Movies", "")

# Remove listed_in column that is no longer needed
genre_data = genre_data.drop(columns=['listed_in'])

print(genre_data.head())



# Filters


st.sidebar.header("""Filters:""")

genre_keuze = st.sidebar.selectbox(
    "Kies een genre:",
    sorted(genre_data["genre"].unique())
)

min_score = st.sidebar.slider(
    "Minimale IMDb-score:",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.5
)

alleen_films = st.sidebar.checkbox(
    "Alleen films tonen"
)

alleen_shows = st.sidebar.checkbox(
    "Alleen series tonen"
)



# Data filteren


filtered_data = genre_data[
    (genre_data["genre"] == genre_keuze) &
    (genre_data["imdb_score"] >= min_score)
]

if alleen_films and not alleen_shows:
    filtered_data = filtered_data[
        filtered_data["type"] == "MOVIE"
    ]

elif alleen_shows and not alleen_films:
    filtered_data = filtered_data[
        filtered_data["type"] == "SHOW"
    ]


st.header("Deel 3: Visueel data bestuderen")


# Grafiek
with st.expander("Dataset filteren en door grafieken bestuderen", expanded=True):
    st.write("""Nadat deze stap is voltooid, kunnen we eindelijk een voorlopige grafiek maken van de verschillen in scores tussen tv-series en films, per genre.""")
    st.write("""Met de filters in de zijbalk hebben we een grafiek en een tabel gemaakt waarmee we beide soorten media voor elk gewenst genre kunnen bestuderen.""")

fig = px.histogram(
    filtered_data,
    x="imdb_score",
    color="type",
    range_x=[0, 10],
    title=f"IMDb-scoreverdeling voor {genre_keuze}"
)

fig.update_traces(xbins=dict(start=0, end=10, size=0.5), marker_line_color="black", marker_line_width=1)

st.plotly_chart(fig, use_container_width=True)



# Tabel


st.subheader("Gefilterde titels")

st.dataframe(
    filtered_data,
    use_container_width=True
)

# Een snelle visualisatie van de totale waarden per categorie laat ons ook het eindresultaat van de filtering zien, aangezien het belangrijk is om te zien wat opvalt. Drama's en Categorieën zijn bijvoorbeeld de twee grootste categorieën, omdat sommige items in de oorspronkelijke dataset meerdere genres hadden. Om te voorkomen dat we handmatig een 'primair' genre voor elk item moesten kiezen, werd besloten dat een item één keer zou tellen voor elk genre waartoe het behoorde. Dus als een film bijvoorbeeld 'Action & Adventure' was en *ook* 'Drama', zou er één item aan beide categorieën worden toegevoegd.

# %%



# Middenstuk: genreverdeling
# Aantal titels per genre

st.subheader("Aantal titels per genre")
with st.expander("""Grafiek: "Genreverdeling van media" uitleg""", expanded=True):
    st.write("""
    We moeten echter niet alleen rekening houden met de verdeling, maar ook met de samenstelling en het totaal aantal vermeldingen per genre in onze dataset.
    Om dit zo goed mogelijk te visualiseren, hebben we onderstaand staafdiagram gemaakt.
    Om mogelijke problemen bij de categorisatie te voorkomen, hebben we ervoor gezorgd dat als een vermelding meerdere genres uit de door ons gekozen filterlijst bevat, deze als een voor elk genre wordt geteld.
    """)
genre_counts = genre_data["genre"].value_counts().sort_values()

figGenre = px.bar(x = genre_counts.index,
                   y = genre_counts.values,
                  labels = {"x": "Genre", "y": "Count"}, 
                  color = genre_counts.index, 
                  title = "Genreverdeling van media")
figGenre.update_traces(width=0.8, marker_line_color="black", marker_line_width=1)
st.plotly_chart(figGenre, use_container_width=True)

with st.expander("""Grafiek: "Genreverdeling van media" conclusie""", expanded=True):
    st.write("""De oude grafiek toont vergelijkingen per serie weliswaar goed in één grafiek, maar de schalen die per sectie worden gebruikt,
    kunnen de algehele verdeling moeilijk leesbaar maken, vooral wanneer zowel een serie als een film worden weergegeven,
    omdat de kolommen dan niet over elkaar heen liggen. Dit kan de leesbaarheid van de grafiek beïnvloeden.
    Daarom wordt de "facetgrafiek"-methode van Plotly gebruikt om één overkoepelende grafiek te maken, waarbij elke combinatie een eigen subgrafiek vormt.
    """)

# Vanwege de variabelen waarmee gewerkt wordt, is een histogram de beste optie om de verdeling van IMDb-scores per genre weer te geven. De x-as is ingesteld op 0 tot 10, voor het bereik van de scores, gesorteerd in intervallen van 0,5. De y-as geeft het aantal weer, dus hoeveel items er per interval zijn. Vanwege het aantal grafieken dat getekend moet worden, moeten er echter enkele aanpassingen worden gedaan.
# 
# Eerstens is de y-as voor elke grafiek onafhankelijk gemaakt, zodat de categorieën Drama en Komedie de leesbaarheid van categorieën met een lager totaal aantal items (zoals Sci-Fi) niet belemmeren. Daarnaast is elke as gelabeld voor een betere leesbaarheid, zodat elke grafiek afzonderlijk kan worden bekeken.

# %%
st.subheader("Eend-grafiek: Histogram van genre-/scorebeoordelingen, gesorteerd op type.")
with st.expander("""Waarom nieuwe grafiek?""", expanded=True):
    st.write("""In een staafdiagram is elke verdeling gemakkelijk af te lezen.
    Zodra er echter vergelijkingen per genre worden gemaakt, wordt de grafiek plotseling moeilijker leesbaar.
    Dit kan komen door het verschil in schaal of doordat de staven naast elkaar staan in plaats van over elkaar heen.
    Daarom wordt er gebruikgemaakt van een "facetgrafiek" om één overkoepelende grafiek te maken, waarbij elke combinatie een eigen subgrafiek vormt.
    """)

with st.expander("Wijzigingen aangebracht in de nieuwe grafiek", expanded=True):
    st.write("""Naast het feit dat elke genre/type-combinatie een eigen subgrafiek heeft, zijn er enkele opmaakwijzigingen doorgevoerd.
    De x-as loopt van 0 tot 10 en geeft het bereik van scores weer, gesorteerd in intervallen van 0,5.
    De y-as geeft het aantal weer, oftewel hoeveel items er per interval zijn.""")
    st.write("""Daarnaast is de y-as voor elke grafiek onafhankelijk gemaakt, zodat de grootste categorieën, `Drama` en `Comedy`,
    de leesbaarheid van andere, kleinere categorieën niet veranderen. Elke as is ook voorzien van een label, zodat elke grafiek afzonderlijk kan worden bekeken.""")
    
fig = px.histogram(genre_data, x = "imdb_score", range_x = [0, 10], color = "type", facet_row = "genre", facet_col = "type",
    category_orders = {"genre": genre_data["genre"].sort_values(),"type": ["MOVIE", "SHOW"]},title = "IMDb-scoreverdeling per genre en type")

# Each x axis range set [0, 10], forced to be set with bins of 0.5 -> Guarantees consistent x axis among all graphs.
fig.update_traces(xbins = dict(start = 0, end = 10, size = 0.5), marker_line_color="black", marker_line_width=1)

# Independent axis scales
fig.update_yaxes(matches = None)

# Show axis labels on every subplot
fig.update_xaxes(showticklabels = True)
fig.update_yaxes(showticklabels = True)

# Width 1500 on Python doc for better spread, 1200 on Notebook doc because Jupyter Notebook cells are too thin to hold all the graphs if wider than 1200
fig.update_layout(height = 2000, width = 1000)

st.plotly_chart(fig, use_container_width=True)


mean_count_scores = genre_data.pivot_table(
    index="genre",
    columns="type",
    values="imdb_score",
    aggfunc=["mean", "count"]
).round(2)


with st.expander("Tabel met de gemiddelde score en het totaal aantal per genre, per type", expanded=True):
    st.write("Om de spreidingen van de grafieken beter te kunnen analyseren, hebben we een `pivot_table()` gemaakt met de gemiddelde scores en hun counts per subplot.")
    st.write(mean_count_scores)
    


# %%
#conclusie
st.header("Deel 4: Conclusies")


with st.expander("Conclusie 1: Steekproefomvang verschillen en het effect dat dit kan hebben", expanded=True):
    st.write("""
    De eerste belangrijke conclusie die uit de grafieken kan worden getrokken, is dat sommige genres sterker vertegenwoordigd zijn in de dataset dan andere.
    Dit is belangrijk voor de interpretatie van de overige resultaten, aangezien genres met meer titels ook meer beoordelingen krijgen,
    waardoor de spreiding van de scores 'natuurlijker' lijkt.
    In combinatie met een klein aantal titels hebben deze uitschieters een groter effect.""")

with st.expander("Conclusie 2: Verschil in gemiddelden, geacht op aantal scores", expanded=True):
    st.write("""De andere conclusie is dat tv-series gemiddeld beter presteren dan films, maar ook minder beoordelingen krijgen.
    Dit is te zien door de gemiddelden in de tabel te vergelijken met de y-as van elke grafiek.
    De gemiddelden van tv-series liggen doorgaans hoger, terwijl de maxima op de y-as lager liggen. 
    Verder statistisch onderzoek zou nodig zijn om te bepalen of dit verschil statistisch relevant is.
    """)

with st.expander("Conclusie 3: Verschillende, kleinere observaties", expanded=True):
    st.write("Observatie 1: De dataset bevat veel meer films dan tv-series.")
    st.write("Observatie 2: `Thriller` shows hebben het beste gemiddelde score op IMDb, maar zijn ook de kleinste categorieën.")
    st.write("Observatie 3: Met uitzondering van het genre `Thriller` bevat elke categorie gemiddeld ongeveer 3 tot 4 keer zoveel films als tv-series.")



# %%




