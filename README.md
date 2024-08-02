# AAPL Stock Market Data Pipeline
## Brief Description of "AAPL Stock Market Data Pipeline"
The "AAPL Stock Market Data Pipeline" project is an advanced, end-to-end data infrastructure solution built using Docker. This project efficiently consumes **real-time stock data** for Apple Inc. (AAPL) from Yahoo Finance and loads it into **Minio**, a high-performance object storage system compatible with Amazon S3. The data is then processed using a robust **Spark application within a Docker container** and subsequently stored in a PostgreSQL database.

A key feature of this project is the integration with **Metabase**, a powerful business intelligence tool, which facilitates dynamic and customizable data visualizations. The user-friendly dashboard offers a comprehensive suite of visualizations, allowing users to delve into and analyze AAPL stock market trends in real-time. Additionally, the pipeline includes a custom notifier that uses **Slack** to provide real-time updates on the pipeline's status, ensuring seamless monitoring and prompt issue resolution.

This project showcases expertise in containerization, real-time data ingestion, big data processing, and data visualization, making it an attractive demonstration of cutting-edge data engineering and analytical skills.


## Installation
### Pre-requisites
1. Ensure you have docker installed in your system https://docs.docker.com/engine/install

   How to verify in your terminal:
   ```bash
   docker-compose version
   ```
   
3. Ensure you have astronomer CLI installed in your system https://www.astronomer.io/docs/astro/cli/install-cli

   How to verify in your terminal:
   ```bash
   astro version
   ```

## Steps
1. Git clone this repo
   ```bash
   git clone stock-market-data-pipeline.git
   ```
2. Navigate to your repo
   ```bash
   cd stock-market-data-pipeline
   ```
3. Start the project
 ```bash
   astro dev start
   ```















   © Haji Rufai
