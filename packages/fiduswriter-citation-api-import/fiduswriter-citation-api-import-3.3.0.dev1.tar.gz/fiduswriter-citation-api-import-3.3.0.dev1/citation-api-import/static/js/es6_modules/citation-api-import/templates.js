import {escapeText} from "../common"

export let searchApiTemplate = () =>
`<div id="bibimport-api-search" title="${gettext("Search bibliography databases")}">
        <p>
            <input id="bibimport-search-text" class="linktitle" type="text" value=""
                    placeholder="${gettext("Title, Author, DOI, etc.")}"/>
            <button id="bibimport-search-button" class="fw-button fw-dark" type="button">
                ${gettext("search")}
            </button>
        </p>
        <div id="bibimport-search-header"></div>
        <div id="bibimport-search-result-sowiport" class="bibimport-search-result"></div>
        <div id="bibimport-search-result-datacite" class="bibimport-search-result"></div>
        <div id="bibimport-search-result-crossref" class="bibimport-search-result"></div>
</div>`


export let searchApiResultSowiportTemplate = ({items}) =>
    items.map(item =>
        `<div class="item">
            <button type="button" class="api-import fw-button fw-orange fw-small"
                    data-id="${item.id}">${gettext('Import')}</button>
            <h3>
                ${escapeText(item.title_full)}
            </h3>
            ${
                item.person_author_txtP_mv ?
                `<p>
                    <b>${gettext('Author(s)')}:</b>
                    ${item.person_author_txtP_mv.join("; ")}
                </p>` :
                ''
            }
            ${
                item.publishDate ?
                `<p><b>${gettext('Published')}:</b> ${item.publishDate[0]}</p>` :
                ''
            }
            ${
                item.doi ?
                `<p><b>DOI:</b> ${item.doi}</p>` :
                ''
            }
            ${
                item.description ?
                `<p>
                    ${
                        item.description.length < 200 ?
                        escapeText(item.description) :
                        escapeText(item.description.substring(0, 200)) + "..."
                    }
                </p>` :
                ''
            }
        </div>`
    ).join('')


export let searchApiResultDataciteTemplate = ({items}) =>
    items.map(item =>
        `<div class="item">
            <button type="button" class="api-import fw-button fw-orange fw-small"
                    data-id="${item.id}" data-doi="${item.attributes.doi}">
                ${gettext('Import')}
            </button>
            <h3>
                ${escapeText(item.attributes.title)}
            </h3>
            ${
                item.attributes.author ?
                `<p>
                    <b>${gettext('Author(s)')}:</b>
                    ${
                        item.attributes.author.map(author =>
                             author.literal ?
                             author.literal :
                             `${author.family} ${author.given}`
                         ).join(", ")
                     }
                </p>` :
                ''
            }
            ${
                item.attributes.published ?
                `<p><b>${gettext('Published')}:</b> ${item.attributes.published}</p>` :
                ''
            }
            ${
                item.attributes.doi ?
                `<p><b>DOI:</b> ${item.attributes.doi}</p>` :
                ''
            }
            ${
                item.attributes.description ?
                `<p>
                    ${
                        item.attributes.description.length < 200 ?
                        escapeText(item.attributes.description) :
                        escapeText(item.attributes.description.substring(0, 200)) + "..."
                    }
                </p>` :
                ''
            }
        </div>`
    ).join('')


export let searchApiResultCrossrefTemplate = ({items}) =>
    items.map(item =>
        `<div class="item">
            <button type="button" class="api-import fw-button fw-orange fw-small"
                    data-doi="${item.doi}">
                ${gettext('Import')}
            </button>
            <h3>
                ${
                    item.fullCitation ?
                    item.fullCitation :
                    `${item.title} ${item.year}`
                }
            </h3>
            ${
                item.doi ?
                `<p><b>DOI:</b> ${item.doi}</p>` :
                ''
            }
            ${
                item.description ?
                `<p>
                    ${
                        item.description.length < 200 ?
                        escapeText(item.description) :
                        escapeText(item.description.substring(0, 200)) + "..."
                    }
                </p>` :
                ''
            }
        </div>`
    ).join('')
