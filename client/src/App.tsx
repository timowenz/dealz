import { useState } from "react";
import { Input } from "./components/ui/input";
import axios, { AxiosError } from "axios";
import { LoaderCircleIcon } from "lucide-react";

type ProductNameSearchResults = {
  [merchant: string]: {
    url: string;
    price: number | null;
  };
};

type ProductNameSearch = {
  productName: string;
  results: ProductNameSearchResults;
};

export default function App() {
  const [input, setInput] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ProductNameSearch | null>(null);

  async function submitProductNameSearch(e: { preventDefault: () => void }) {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await axios.get(
        `http://localhost:8000/api/v1/browser/${input}`
      );

      const data: ProductNameSearch = response.data;
      console.log(data);
      setData(data);
    } catch (err) {
      console.log(err);
      if (err instanceof AxiosError) {
        console.error(err.message);
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center gap-5">
      <h1 className="text-4xl font-bold">Dealz</h1>
      <form onSubmit={submitProductNameSearch} className="w-[30%] rounded-md">
        <Input
          placeholder="Enter product name"
          onChange={(e) => {
            setError(null);
            setInput(e.target.value);
          }}
        ></Input>
      </form>

      {isLoading && (
        <div className="flex items-center gap-1">
          <p>Searching</p>
          <LoaderCircleIcon className="animate-spin" />
        </div>
      )}
      {error && <div className="text-red-500">An error occured: {error}</div>}

      {data && <MerchantResult {...data} />}
    </div>
  );
}

function MerchantResult(data: ProductNameSearch) {
  function centToEuro(cents: number): string {
    return (cents / 100).toFixed(2);
  }

  return (
    <div>
      <p className="text-center">Product: {data.productName}</p>
      <br />
      <ul className="flex flex-col gap-2.5">
        {data.results &&
        typeof data.results === "object" &&
        Object.keys(data.results).length > 0 ? (
          Object.entries(data.results)
            .sort(([, a], [, b]) => {
              if (a.price === null && b.price === null) return 0;
              if (a.price === null) return 1;
              if (b.price === null) return -1;
              return a.price - b.price;
            })
            .map(
              ([key, result]: [
                string,
                { url: string; price: number | null }
              ]) => (
                <li key={key} className="flex gap-2.5 border rounded-md p-4">
                  <div>
                    Price:{" "}
                    {result.price === null
                      ? "Not available"
                      : `${centToEuro(result.price)} €`}
                  </div>
                  <div>
                    Link:{" "}
                    <a
                      href={result.url}
                      className="text-blue-600 underline"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {result.url}
                    </a>
                  </div>
                </li>
              )
            )
        ) : (
          <li>No results found.</li>
        )}
      </ul>
    </div>
  );
}
