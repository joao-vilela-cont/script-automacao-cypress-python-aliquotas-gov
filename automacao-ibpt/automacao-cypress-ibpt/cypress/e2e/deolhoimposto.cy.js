import Constants from "../utils/Constants";
Cypress.on('uncaught:exception', (err, runnable) => { return false })

describe('Automação IBPT', () => {
  it('Logar no site e Verificar versão disponível para Download', () => {
    logar();
    checkVersion();
  });
});

function checkVersion() {
  cy.get(Constants.INPUT_ULTIMA_VERSAO_INSTALADA).invoke('text').then((versionUltimaInstalada) => {
    cy.get(Constants.INPUT_ULTIMA_VERSAO_DISPONIVEL).invoke('text').then((ultimaDisponivelParaDownload) => {
      const versionString = ultimaDisponivelParaDownload.match(/Baixar tabela - Versão (\d+(\.\d+)*\.\w+)/);
      const versionNumberUtimaBaixar = versionString[1];
      if (versionUltimaInstalada === versionNumberUtimaBaixar) {
        return;
      } else {
        getNovaVersion();
      }
    });
  });
}

function logar() {
  cy.visit(Constants.URL_ENTRAR_LOGIN);
  clicarElementoEPreencher('#Email', Constants.USER);
  clicarElementoEPreencher('#Senha', Constants.PASSWORD);
  clicarElemento('.btn-success');
}

function getNovaVersion () {
  clicarElemento(Constants.BUTTON_NOVA_TABELA);
  selectAllEstados();
  clicarElemento(Constants.BUTTON_CONFIRMAR);
  cy.visit(Constants.URL_TABELA_IMPOSTO);
  aguardarParaClicarElemento(Constants.BUTTON_DOWNLOAD);
}

function selectAllEstados() {
  cy.get('.search-choice-close').click();
  cy.get('.search-field').click(); 
  cy.get('.chosen-results li').then($options => {
    for (let i = 0; i < 27; i++) {
        cy.get(`[data-option-array-index=${i}]`).click();
        cy.get('.search-field').click(); 
    }
  });
}

function scrollTo(element) {
  cy.get(element).scrollIntoView()
}

function clicarElementoEPreencher(locator, text, option) {
  scrollTo(locator)
  cy.get(locator).click(option).type(text, option)
}

function clicarElemento(locator, option) {
  scrollTo(locator)
  cy.get(locator, { timeout: 10000 }).click(option)
}

function aguardarParaClicarElemento(locator) {
  cy.wait(Constants.WAIT_RESPOSTA_GOVERNO)
  cy.get(locator).invoke('text').then((text) => {
    if(text === "Download") {
      cy.get(locator).click()
    } else {
      aguardarParaClicarElemento(Constants.BUTTON_DOWNLOAD);
    }
  })
}
