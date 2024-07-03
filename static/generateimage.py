from html2image import Html2Image
def image_from_html(filename,
                    posPerc,
                    neuPerc,
                    negPerc,
                    posCant,
                    neuCant,
                    negCant,
                    pos_avg_conf,
                    neu_avg_conf,
                    neg_avg_conf,
                    pos_dist,
                    neu_dist,
                    neg_dist,
                    adjs,
                    stats):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Resumen de datos para a</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@400..900&display=swap" rel="stylesheet">

    </head>
    <body>
    <h1>{filename}</h1>

    <div class="container-stats">

        <p class="tittle">The polarized sentiment distribution is:</p>

        <div class="perc-graphic">
            <div class="bar" style="--width: 100%; --color: #7b7b7b; --left: 0"></div>
            <div class="bar" style="--width: {posPerc}%; --color: #00ff00; --left: 0"></div>
            <div class="bar" style="--width: {negPerc}%; --color: #ff4646ff; right:0"></div>
        </div>

        <div class="label-perc-graphic">
            <div class="label-text">
                <span class="feeling-text">positive:</span>
                <span class="orange-text">{posPerc}%</span> - <span class="yellow-text">[{posCant}]</span>
            </div>

            <div class="label-text">
                <span class="feeling-text">neutral:</span>
                <span class="orange-text">{neuPerc}%</span> - <span class="yellow-text">[{neuCant}]</span>
            </div>

            <div class="label-text">
                <span class="feeling-text">negative:</span>
                <span class="orange-text">{negPerc}%</span> - <span class="yellow-text">[{negCant}]</span>
            </div>
        </div>

        <br>
        <p class="tittle">Average confidence of the predictions of each sentiment:</p>

        <div class="avg-confidence-graphic">
            <div class="progress-bar" style="--progress: {pos_avg_conf*100}%; --color: #00ff00" data-text="positive: {pos_avg_conf}"></div>
            <div class="progress-bar" style="--progress: {neu_avg_conf*100}%; --color: #7b7b7b" data-text="neutral: {neu_avg_conf}"></div>
            <div class="progress-bar" style="--progress: {neg_avg_conf*100}%; --color: #ff4646ff" data-text="negative: {neg_avg_conf}"></div>
        </div>
        <br>
    </div>
    <div class="second-half">
            <div class="second-half-column">
                <p class="tittle">Weighted distribution of each sentiment</p>
                <hr>
                <div class="full-graph">
                    <div class="distrib-graphic"></div>
                    <div class="distrib-leyend">
                        <p><span style="color:#00ff00">{pos_dist}%</span> - <span style="color:#adadad">{neu_dist}%</span> - <span style="color:#ff4646ff">{neg_dist}%</span></p>
                    </div>
                </div>
            </div>

            <div class="second-half-column">
                <p class="tittle">Text content<br>statistics</p>
                <hr>
                <p><span class="adjectives orange-text">{stats[0]}</span> analized texts</p>
                <p><span class="adjectives yellow-text">{stats[1]}</span> words</p>
                <p><span class="adjectives purple-text">{stats[2]}</span> adjectives</p>
                <p><span class="adjectives orange-text">{stats[3]}</span> words per text</p>
            </div>

            <div class="second-half-column">
                <p class="tittle">Most repeated<br>adjectives</p>
                <hr>
                <p class="tittle"><span class="yellow-text">{list(adjs.keys())[0]}</span> - [{list(adjs.values())[0]}]</p>
                <p class="tittle"><span class="yellow-text">{list(adjs.keys())[1]}</span> - [{list(adjs.values())[1]}]</p>
                <p class="tittle"><span class="yellow-text">{list(adjs.keys())[2]}</span> - [{list(adjs.values())[2]}]</p>
                <p class="tittle"><span class="yellow-text">{list(adjs.keys())[3]}</span> - [{list(adjs.values())[3]}]</p>
                <p class="tittle"><span class="yellow-text">{list(adjs.keys())[4]}</span> - [{list(adjs.values())[4]}]</p>
            </div>
    </div>
    

</body>
    </html>
    """
    css = f"""body {{
            font-family: "Gabarito", sans-serif;
            font-style: normal;
            font-weight: 600;
            font-size: larger;
            text-align: center;
            color: white;
            margin: 0 auto;
            height: 1000px;
            width: 1000px;
            background-color: #26355dff;
        }}

        h1 {{
            padding-top: 40px;
            color: #ff8f00;
        }}

        .orange-text {{
            color: #ff8f00;
        }}

        .yellow-text {{
            color: #ffdb00;
        }}

        .purple-text {{
            color: #8f50c0;
        }}

        .tittle {{
            font-size: 800;
            font-size: x-large;
        }}

        .container-stats {{
            background-color: #9050c07b;
            padding: 3px;
            border-radius: 10px;
            margin-left: 3%;
            margin-right: 3%;
        }}

        .perc-graphic {{
            width: 95%; /* Ocupa todo el ancho disponible */
            height: 40px; /* Ajusta la altura según tus necesidades */
            margin: 0 auto; /* Centra el contenedor horizontalmente */
            display: flex; /* Usar flexbox para la distribución horizontal */
            position: relative; /* Posicionamiento relativo para superponer */
            border-radius: 5px; /* Redondea las esquinas */
        }}

        .bar {{
            left: var(--left);
            position: absolute;
            width: var(--width);
            height: 100%;
            background-color: var(--color);
            top: 0;
        }}

        .label-perc-graphic {{
            display: flex; /* Usar flexbox para la cuadrícula */
            flex-wrap: wrap; /* Permitir que los elementos se envuelvan en varias filas */
            width: 95%; /* Ajustar el ancho al contenido */
            margin: 0 auto; /* Centrar la cuadrícula horizontalmente */
            padding-top: 15px;
        }}

        .label-text {{
            flex: 1 0 30%; /* Dividir el espacio equitativamente */
            text-align: center; /* Centrar el texto horizontalmente */
        }}

        .avg-confidence-graphic {{
            display: flex; /* Coloca las barras en línea */
            justify-content: space-around; /* Distribuye uniformemente */
            margin: 0 auto;
            width: 95%;
        }}

        .progress-bar {{
            width: 260px; 
            height: 40px;
            background-color: rgba(0, 0, 0, 0.464); 
            border-style: solid black;
            border-radius: 5px;
            position: relative; 
            margin: 5px;
        }}

        .progress-bar::before {{
            content: attr(data-text); 
            position: absolute;
            top: 50%; /* Centrar verticalmente */
            left: 50%;
            transform: translate(-50%, -50%); /* Centrar horizontal y verticalmente */
            color: white; /* Color del texto para que sea visible */
            z-index: 1; /* Asegurar que el texto esté por encima */
        }}

        .progress-bar::after {{
            content: "";
            display: block;
            height: 100%;
            width: var(--progress); 
            background-color: var(--color); 
        }}

        .second-half {{
            display: flex;
            flex-wrap: wrap;
            margin: 0 auto;
            width: 95%;
        }}

        .second-half-column {{
            flex: 1 0 20%;
            flex-wrap: wrap;
            margin: 5px;

        }}

        .adjectives {{
            font-size: xx-large;
        }}

        .distrib-graphic {{
            margin: 0 auto;
            margin-top: 5%;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: conic-gradient( #00ff00 {pos_dist}%,
                                        #7b7b7b {pos_dist}% {pos_dist+neu_dist}%,
                                        #ff4646ff {pos_dist+neu_dist}%);
        }}

        .distrib-leyend p {{
            width: 220px; 
            background-color: rgba(0, 0, 0, 0.462); 
            padding: 5%;
            border-radius: 5px;
            position: flex; 
            margin: 5% auto;
            text-align: center;
        }}

        """

    html_str = str(html)
    css_str = str(css)

    hti = Html2Image(size=(1000, 900), output_path='static/outputs/')
    hti.screenshot(html_str=html_str, css_str=css_str, save_as='image.jpg')

if __name__ == '__main__':
    print("Convirtiendo a imagen")
