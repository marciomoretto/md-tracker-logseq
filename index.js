async function main() {
  // Registra um comando chamado "Say Hello"
  logseq.App.registerCommandPalette(
    {
      key: "nautilus",
      label: "Nautilus",
      keybinding: {
        binding: "ctrl+shift+n", // Define o atalho corretamente
        mode: "global", // Certifica-se de que funciona globalmente
      },
    },
    async () => {
      // Obtém a página corrente
      const currentPage = await logseq.Editor.getCurrentPage();

      if (!currentPage) {
        logseq.App.showMsg("❌ Nenhuma página encontrada");
        return;
      }

      // Determina se é um Journal ou uma Page
      let pageType = "page"; // Assume que é uma página padrão por default
      let pageName = currentPage.originalName;

      // Verifica se a página é um Journal (baseado na convenção de datas no nome)
      if (currentPage?.journalDay) {
        pageType = "journal";
        const [day, month, year] = currentPage.originalName.split("-");
        pageName = `${year}_${month}_${day}`;
      }

      // URL para chamada HTTP
      const url = `http://localhost:5000/run-script?type=${pageType}&name=${encodeURIComponent(pageName)}`;

      try {
        // Faz a requisição HTTP
        const response = await fetch(url);
        if (response.ok) {
          const result = await response.text(); // Obtém a resposta do servidor
         
          const noFileRegex = /Nenhum arquivo encontrado com o nome da página/;
          if (noFileRegex.test(result)) {
            logseq.App.showMsg("✅ Nenhum arquivo vinculado a esta página");
          } else {
            logseq.App.showMsg(`✅ Script executed: ${result}`);
          }
        } else {
          logseq.App.showMsg(`❌ Failed to execute script: ${response.statusText}`);
        }
      } catch (error) {
        logseq.App.showMsg(`❌ Error: ${error.message}`);
      }

    }
  );

  logseq.App.showMsg("Nautilus plugin is loaded!");
}

logseq.ready(main).catch(console.error);


