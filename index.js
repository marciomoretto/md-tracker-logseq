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

      pageName = currentPage?.originalName || "Unknown Page";

      // Verifica se a página é um Journal (baseado na convenção de datas no nome)
      if (currentPage?.journalDay) {
        // Título do Journal com formatação
        const journalDate = new Date(
          parseInt(currentPage.journalDay, 10) * 1000 // Convertendo o Unix Timestamp
        ).toLocaleDateString("pt-BR", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });

        pageName = `Journal - ${journalDate}`;
      }

      if (!currentPage) {
        logseq.App.showMsg("❌ Nenhuma página encontrada");
        return;
      }      

      // URL para chamada HTTP
      const url = `http://localhost:5000/run-script?pagename=${encodeURIComponent(pageName)}`;

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


