using OpenAI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.VectorData;
using CommunityToolkit.VectorData.InMemory;

Console.WriteLine("Hello, World!");

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

var files = Directory.GetFiles("docs", "*.md");

foreach (var file in files)
{
    var text = await File.ReadAllTextAsync(file);
    Console.WriteLine($"Loading file {file}...");
    // chunk + embed next
    var v = await embedder.GenerateAsync(text);




    await pages.UpsertAsync(new PageChunk {
        Id = Guid.NewGuid().ToString(),
        Text = text, Url = file,
        Embedding = v.Vector });

}








public class PageChunk
{
    [VectorStoreKey]  public string Id { get; set; } = "";
    [VectorStoreData] public string Text { get; set; } = "";
    [VectorStoreData] public string Url { get; set; } = "";
    [VectorStoreVector(1536)]
    public ReadOnlyMemory<float> Embedding { get; set; }
}

