// ==UserScript==
// @name         Extrair Episódios Globoplay
// @namespace    http://tampermonkey.net/
// @version      1.3.0
// @description  Extrai dados dos episódios e extras (trailers, making of etc.) no Globoplay e exporta em JSON, com contador e botão de copiar direto da tela
// @author       GPT
// @match        https://globoplay.globo.com/*/t/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    function formatTitulo(titulo) {
        return titulo.replace(/\s*\/\s*/g, ' / ').trim();
    }

    function obterTituloSerie() {
        const titleTag = document.querySelector('title');
        if (!titleTag) return 'Série Desconhecida';
        return titleTag.textContent.replace(': assista agora!', '').trim();
    }

    function obterTotalCapitulos() {
        const totalEl = document.querySelector('.page-selector__total-chapters');
        if (!totalEl) return null;
        const match = totalEl.textContent.match(/\d+/);
        return match ? parseInt(match[0]) : null;
    }

    function extrairEpisodios() {
        const episodios = [];

        // Seletores possíveis (episódios normais ou extras)
        const itens = document.querySelectorAll(
            'ol.title-episodes-seasoned-offer__episodes > li, \
             .title-episodes-list-offer .title-episode, \
             .inactive-epg-soap-opera-episodes .title-episode, \
             .offer-slider .video-thumb' // novo seletor para "extras"
        );

        if (!itens.length) {
            alert('⚠ Nenhum episódio encontrado. Verifique se a página carregou completamente.');
            return;
        }

        itens.forEach((el) => {
            const isExtra = el.classList.contains('video-thumb');

            let linkElement, imgElement, titulo, sinopse;

            if (isExtra) {
                // Estrutura usada em "extras" (trailers, etc)
                linkElement = el.querySelector('a.video-thumb__link');
                imgElement = el.querySelector('img.video-thumb__cover');

                const desc = el.querySelector('.video-thumb__description span');
                const headline = el.querySelector('.video-thumb__headline span');

                sinopse = desc ? desc.textContent.trim() : '';
                titulo = headline ? headline.textContent.trim() : sinopse || 'Extra';
            } else {
                // Estrutura usada em episódios normais
                linkElement = el.querySelector('.video-widget a');
                imgElement = el.querySelector('.thumbnail-widget img.thumb');

                const tituloElement = el.querySelector('.title-episode__title') || el.querySelector('.video-widget a[title]');
                const sinopseElement = el.querySelector('.title-episode__description span') || el.querySelector('.thumbnail-widget img.thumb[alt]');

                const textoTitulo = tituloElement?.textContent?.trim();
                if (textoTitulo && /^\d+\./.test(textoTitulo)) {
                    titulo = textoTitulo.substring(textoTitulo.indexOf('.') + 1).trim();
                } else {
                    titulo = tituloElement?.getAttribute('title') || textoTitulo || 'Episódio';
                }

                sinopse = sinopseElement?.textContent?.trim() || imgElement?.alt || '';
            }

            if (linkElement && imgElement) {
                episodios.push({
                    numero: (episodios.length + 1).toString().padStart(3, '0'),
                    titulo: formatTitulo(titulo),
                    sinopse: sinopse,
                    capa: imgElement.src,
                    link: linkElement.href,
                    tipo: isExtra ? 'extra' : 'episodio'
                });
            }
        });

        const serieTitulo = obterTituloSerie();
        const jsonFinal = {
            serie_title: serieTitulo,
            quantidade: episodios.length,
            episodios: episodios
        };

        mostrarResultado(JSON.stringify(jsonFinal, null, 2));
    }

    function mostrarResultado(json) {
        let container = document.getElementById('json-output-container');
        if (container) container.remove();

        container = document.createElement('div');
        container.id = 'json-output-container';
        Object.assign(container.style, {
            position: 'fixed',
            bottom: '20px',
            left: '20px',
            zIndex: '9999',
            background: 'white',
            border: '1px solid #ccc',
            padding: '10px',
            boxShadow: '0 0 10px rgba(0,0,0,0.3)',
            maxWidth: '600px',
            width: '90%'
        });

        const textarea = document.createElement('textarea');
        textarea.value = json;
        textarea.rows = 20;
        Object.assign(textarea.style, {
            width: '100%',
            fontFamily: 'monospace'
        });

        const botoesDiv = document.createElement('div');
        Object.assign(botoesDiv.style, { marginTop: '10px', display: 'flex', gap: '10px', flexWrap: 'wrap' });

        const downloadBtn = document.createElement('button');
        downloadBtn.textContent = '💾 Baixar JSON';
        Object.assign(downloadBtn.style, {
            padding: '5px 10px',
            cursor: 'pointer'
        });
        downloadBtn.onclick = () => {
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'globoplay_trailers.json';
            a.click();
            URL.revokeObjectURL(url);
        };

        const copiarBtn = document.createElement('button');
        copiarBtn.textContent = '📋 Copiar JSON';
        Object.assign(copiarBtn.style, {
            padding: '5px 10px',
            cursor: 'pointer'
        });
        copiarBtn.onclick = async () => {
            await navigator.clipboard.writeText(json);
            copiarBtn.textContent = '✅ Copiado!';
            setTimeout(() => (copiarBtn.textContent = '📋 Copiar JSON'), 1500);
        };

        const fecharBtn = document.createElement('button');
        fecharBtn.textContent = '✖ Fechar';
        Object.assign(fecharBtn.style, {
            padding: '5px 10px',
            cursor: 'pointer'
        });
        fecharBtn.onclick = () => container.remove();

        botoesDiv.appendChild(downloadBtn);
        botoesDiv.appendChild(copiarBtn);
        botoesDiv.appendChild(fecharBtn);

        container.appendChild(textarea);
        container.appendChild(botoesDiv);
        document.body.appendChild(container);
    }

    function adicionarBotao() {
        if (document.getElementById('extrair-episodios-btn')) return;

        const botao = document.createElement('button');
        botao.id = 'extrair-episodios-btn';
        botao.textContent = '📥 Extrair Episódios';
        Object.assign(botao.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            zIndex: '9999',
            padding: '10px',
            backgroundColor: '#0073e6',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '14px'
        });

        botao.addEventListener('click', extrairEpisodios);
        document.body.appendChild(botao);
    }

    // 🔍 Observer atualizado para detectar qualquer tipo de listagem (inclui extras)
    const observer = new MutationObserver((mutations, obs) => {
        if (
            document.querySelector(
                'ol.title-episodes-seasoned-offer__episodes, \
                 .title-episodes-list-offer, \
                 .inactive-epg-soap-opera-episodes, \
                 .offer-slider .video-thumb'
            )
        ) {
            adicionarBotao();
            obs.disconnect();
        }
    });

    // Garante o botão mesmo se a página já estiver carregada
    if (
        document.readyState === 'complete' ||
        document.querySelector(
            '.offer-slider .video-thumb, \
             ol.title-episodes-seasoned-offer__episodes, \
             .title-episodes-list-offer, \
             .inactive-epg-soap-opera-episodes'
        )
    ) {
        adicionarBotao();
    } else {
        observer.observe(document.body, { childList: true, subtree: true });
    }
})();
