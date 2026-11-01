using OpenAI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using CommunityToolkit.VectorData.InMemory;
using System.Text;

var config = new ConfigurationBuilder()
    .AddUserSecrets<Program>()
    .Build();

var openAi = new OpenAIClient(config["OpenAI:Key"]!);

var embedder = openAi
    .GetEmbeddingClient("text-embedding-3-small")
    .AsIEmbeddingGenerator();

var chat = openAi
    .GetChatClient("gpt-4o-mini").AsIChatClient();

var store = new InMemoryVectorStore(
    new() { EmbeddingGenerator = embedder });

var pages = store.GetCollection<string, PageChunk>(
    "site-pages");

await pages.EnsureCollectionExistsAsync();

var files = Directory.GetFiles("docs", "*.md");

foreach (var file in files)
{
    Console.WriteLine($"Loading file {file}...");
    var text = await File.ReadAllTextAsync(file);

    foreach (var chunk in Chunk(text, 1000))
    {
        var v = await embedder.GenerateAsync(chunk);
        await pages.UpsertAsync(new PageChunk
        {
            Id = Guid.NewGuid().ToString(),
            Text = chunk,
            Url = file,
            Embedding = v.Vector
        });
    }
}

while (true)
{
    Console.Write("Question: ");
    var question = Console.ReadLine()!;

    var qv = await embedder.GenerateAsync(question);

    var hits = pages.SearchAsync(qv.Vector, top: 3);

    var context = new StringBuilder();
    await foreach (var hit in hits)
        context.AppendLine(hit.Record.Text);

    var prompt = $"""
    ענה בעברית על השאלה אך ורק בעזרת המידע שמופיע אחרי הכותרת "קונטקסט:".

    ## שאלה: {question}

    ## קונטקסט:  {context}
    """;
    var reply = await chat.GetResponseAsync(prompt);

    Console.WriteLine(reply.Text);
}



static IEnumerable<string> Chunk(string text, int max = 1500)
{
    text = text.Replace("\r\n", "\n");
    var sb = new StringBuilder();
    var paras = text.Split("\n\n",
                    StringSplitOptions.RemoveEmptyEntries);
    foreach (var p in paras)
    {
        if (sb.Length + p.Length > max && sb.Length > 0)
        { yield return sb.ToString(); sb.Clear(); }
        sb.AppendLine(p.Trim());
    }
    if (sb.Length > 0) yield return sb.ToString();
}


public class PageChunk
{
    [VectorStoreKey] public string Id { get; set; } = "";
    [VectorStoreData] public string Text { get; set; } = "";
    [VectorStoreData] public string Url { get; set; } = "";
    [VectorStoreVector(1536)]
    public ReadOnlyMemory<float> Embedding { get; set; }
}
