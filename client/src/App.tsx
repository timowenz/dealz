import { useState } from "react";
import { Input } from "./components/ui/input";
import axios, { AxiosError } from "axios";
import { LoaderCircleIcon } from "lucide-react";

type PriceHistory = {
  price: number | null;
  timestamp: string;
};

type ProductNameSearchResults = {
  [merchant: string]: {
    url: string;
    price: number | null;
    priceHistory: PriceHistory[];
  };
};

type ProductNameSearch = {
  productName: string;
  lowestPrice: number | null;
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
      const VITE_API_URL = import.meta.env.VITE_API_URL;

      const response = await axios.get(
        `${VITE_API_URL}/api/v1/browser/${input}`
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
      {error && <div className="text-red-500">An error occurred: {error}</div>}

      {data && <MerchantResult {...data} />}
    </div>
  );
}

function MerchantResult(data: ProductNameSearch) {
  function centToEuro(cents: number): string {
    return (cents / 100).toFixed(2);
  }

  function formatGermanDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleString("de-DE");
  }

  return (
    <div className="w-[60%]">
      <div className="text-center">
        <p>Product: {data.productName}</p>
        <p>
          Lowest Price:{" "}
          {data.lowestPrice === null || data.lowestPrice === undefined
            ? "N/A"
            : `${centToEuro(data.lowestPrice)} €`}
        </p>
      </div>

      <br />
      <ul className="flex flex-col gap-2.5 justify-center items-center">
        {data.results &&
        typeof data.results === "object" &&
        Object.keys(data.results).length > 0 ? (
          Object.entries(data.results)
            .sort(([, a], [, b]) => {
              if (a.price === null && b.price === null) return 0;
              if (a.price === null) return 1;
              if (b.price === null) return -1;
              return (a.price ?? 0) - (b.price ?? 0);
            })
            .map(([key, result]) => (
              <li
                key={key}
                className="flex flex-col gap-2.5 border rounded-md p-4"
              >
                <div>
                  <span className="font-semibold">{key}</span>
                </div>
                <div>
                  Latest Price:{" "}
                  {result.price === null
                    ? "N/A"
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
                {result.priceHistory &&
                  Array.isArray(result.priceHistory) &&
                  result.priceHistory.length > 0 && (
                    <div className="mt-2">
                      <div className="font-semibold mb-1">Price History:</div>
                      <ul className="text-xs bg-gray-100 rounded p-2 max-h-32 overflow-auto">
                        {result.priceHistory.map((entry, idx2) => (
                          <li key={idx2} className="flex gap-2 justify-between">
                            <span>
                              {entry.price === null || entry.price === undefined
                                ? "N/A"
                                : `${centToEuro(entry.price)} €`}
                            </span>
                            <span className="text-gray-500">
                              {formatGermanDate(entry.timestamp)}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
              </li>
            ))
        ) : (
          <li>No results found.</li>
        )}
      </ul>
    </div>
  );
}
