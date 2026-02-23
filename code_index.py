from dotenv import load_dotenv
import cocoindex


@cocoindex.flow_def(name="CodebaseIndex")
def codebase_index_flow(flow_builder: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope):
    # Source: local files matching specre.toml config (app/ and spec/, .rb .erb .js .jsx)
    data_scope["files"] = flow_builder.add_source(
        cocoindex.sources.LocalFile(
            path=".",
            included_patterns=[
                "app/**/*.rb", "app/**/*.erb", "app/**/*.js", "app/**/*.jsx",
                "spec/**/*.rb", "spec/**/*.erb", "spec/**/*.js", "spec/**/*.jsx",
            ],
        )
    )

    code_embeddings = data_scope.add_collector()

    with data_scope["files"].row() as doc:
        # Detect programming language from filename
        doc["language"] = doc["filename"].transform(
            cocoindex.functions.DetectProgrammingLanguage()
        )

        # Split content into chunks
        doc["chunks"] = doc["content"].transform(
            cocoindex.functions.SplitRecursively(),
            chunk_size=2000,
            chunk_overlap=500,
        )

        with doc["chunks"].row() as chunk:
            # Embed each chunk
            chunk["embedding"] = chunk["text"].transform(
                cocoindex.functions.SentenceTransformerEmbed(
                    model="sentence-transformers/all-MiniLM-L6-v2"
                )
            )

            code_embeddings.collect(
                filename=doc["filename"],
                language=doc["language"],
                location=chunk["location"],
                text=chunk["text"],
                embedding=chunk["embedding"],
            )

    code_embeddings.export(
        "code_embeddings",
        cocoindex.targets.Postgres(),
        primary_key_fields=["filename", "location"],
        vector_indexes=[
            cocoindex.VectorIndexDef(
                field_name="embedding",
                metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY,
            )
        ],
    )


if __name__ == "__main__":
    load_dotenv(".env.cocoindex")
    cocoindex.init()
    codebase_index_flow.update()
