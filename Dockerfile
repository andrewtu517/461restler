# Stage 1: Builder
FROM mcr.microsoft.com/dotnet/sdk:6.0-alpine AS builder

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy necessary files
COPY src ./src
COPY restler ./restler
COPY build-restler.py .

# Build RESTler
RUN python3 build-restler.py --dest_dir /build

# Compile Python files
RUN python3 -m compileall -b /build/engine

# Stage 2: Target
FROM mcr.microsoft.com/dotnet/aspnet:6.0-alpine AS target

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Option 1: Using --break-system-packages (Simpler)
# RUN pip3 install --break-system-packages requests applicationinsights

# Option 2: Using Virtual Environment (Best Practice)
# Uncomment the lines below to use a virtual environment instead
RUN python3 -m venv /opt/venv
RUN /bin/sh -c ". /opt/venv/bin/activate && pip install requests applicationinsights"
ENV PATH="/opt/venv/bin:$PATH"

# Copy the built application from the builder stage
COPY --from=builder /build /RESTler

# Set the entry point (adjust as needed)
ENTRYPOINT ["dotnet", "/RESTler/YourApp.dll"]
