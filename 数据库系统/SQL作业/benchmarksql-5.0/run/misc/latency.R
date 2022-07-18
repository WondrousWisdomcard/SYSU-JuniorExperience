# ----
# R graph to show latency of all transaction types.
# ----

# ----
# Read the runInfo.csv file.
# ----
runInfo <- read.csv("data/runInfo.csv", head=TRUE)

# ----
# Determine the grouping interval in seconds based on the
# run duration.
# ----
xmax <- runInfo$runMins
for (interval in c(1, 2, 5, 10, 20, 60, 120, 300, 600)) {
    if ((xmax * 60) / interval <= 1000) {
        break
    }
}
idiv <- interval * 1000.0

# ----
# Read the result.csv and then filter the raw data
# by transaction type
# ----
rawData <- read.csv("data/result.csv", head=TRUE)
noBGData <- rawData[rawData$ttype != 'DELIVERY_BG', ]
newOrder <- rawData[rawData$ttype == 'NEW_ORDER', ]
payment <- rawData[rawData$ttype == 'PAYMENT', ]
orderStatus <- rawData[rawData$ttype == 'ORDER_STATUS', ]
stockLevel <- rawData[rawData$ttype == 'STOCK_LEVEL', ]
delivery <- rawData[rawData$ttype == 'DELIVERY', ]
deliveryBG <- rawData[rawData$ttype == 'DELIVERY_BG', ]

# ----
# Aggregate the latency grouped by interval.
# ----
aggNewOrder <- setNames(aggregate(newOrder$latency, list(elapsed=trunc(newOrder$elapsed / idiv) * idiv), mean),
		   c('elapsed', 'latency'));
aggPayment <- setNames(aggregate(payment$latency, list(elapsed=trunc(payment$elapsed / idiv) * idiv), mean),
		   c('elapsed', 'latency'));
aggOrderStatus <- setNames(aggregate(orderStatus$latency, list(elapsed=trunc(orderStatus$elapsed / idiv) * idiv), mean),
		   c('elapsed', 'latency'));
aggStockLevel <- setNames(aggregate(stockLevel$latency, list(elapsed=trunc(stockLevel$elapsed / idiv) * idiv), mean),
		   c('elapsed', 'latency'));
aggDelivery <- setNames(aggregate(delivery$latency, list(elapsed=trunc(delivery$elapsed / idiv) * idiv), mean),
		   c('elapsed', 'latency'));

# ----
# Determine the ymax by increasing in sqrt(2) steps until 98%
# of ALL latencies fit into the graph. Then multiply with 1.2
# to give some headroom for the legend.
# ----
ymax_total <- quantile(noBGData$latency, probs = 0.98)

ymax <- 1
sqrt2 <- sqrt(2.0)
while (ymax < ymax_total) {
    ymax <- ymax * sqrt2
}
if (ymax < (ymax_total * 1.2)) {
    ymax <- ymax * 1.2
}



# ----
# Start the output image.
# ----
png("latency.png", width=@WIDTH@, height=@HEIGHT@)
par(mar=c(4,4,4,4), xaxp=c(10,200,19))

# ----
# Plot the Delivery latency graph.
# ----
plot (
	aggDelivery$elapsed / 60000.0, aggDelivery$latency,
	type='l', col="blue3", lwd=2,
	axes=TRUE,
	xlab="Elapsed Minutes",
	ylab="Latency in Milliseconds",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the StockLevel latency graph.
# ----
par(new=T)
plot (
	aggStockLevel$elapsed / 60000.0, aggStockLevel$latency,
	type='l', col="gray70", lwd=2,
	axes=FALSE,
	xlab="",
	ylab="",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the OrderStatus latency graph.
# ----
par(new=T)
plot (
	aggOrderStatus$elapsed / 60000.0, aggOrderStatus$latency,
	type='l', col="green3", lwd=2,
	axes=FALSE,
	xlab="",
	ylab="",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the Payment latency graph.
# ----
par(new=T)
plot (
	aggPayment$elapsed / 60000.0, aggPayment$latency,
	type='l', col="magenta3", lwd=2,
	axes=FALSE,
	xlab="",
	ylab="",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the NewOrder latency graph.
# ----
par(new=T)
plot (
	aggNewOrder$elapsed / 60000.0, aggNewOrder$latency,
	type='l', col="red3", lwd=2,
	axes=FALSE,
	xlab="",
	ylab="",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Add legend, title and other decorations.
# ----
legend ("topleft",
	c("NEW_ORDER", "PAYMENT", "ORDER_STATUS", "STOCK_LEVEL", "DELIVERY"),
	fill=c("red3", "magenta3", "green3", "gray70", "blue3"))
title (main=c(
    paste0("Run #", runInfo$run, " of BenchmarkSQL v", runInfo$driverVersion),
    "Transaction Latency"
    ))
grid()
box()

# ----
# Generate the transaction summary and write it to
# data/tx_summary.csv
# ----
tx_total <- NROW(noBGData)

tx_name <- c(
	'NEW_ORDER',
	'PAYMENT',
	'ORDER_STATUS',
	'STOCK_LEVEL',
	'DELIVERY',
	'DELIVERY_BG',
	'tpmC',
	'tpmTotal')
tx_count <- c(
	NROW(newOrder),
	NROW(payment),
	NROW(orderStatus),
	NROW(stockLevel),
	NROW(delivery),
	NROW(deliveryBG),
	sprintf("%.2f", NROW(newOrder) / runInfo$runMins),
	sprintf("%.2f", NROW(noBGData) / runInfo$runMins))
tx_percent <- c(
	sprintf("%.3f%%", NROW(newOrder) / tx_total * 100.0),
	sprintf("%.3f%%", NROW(payment) / tx_total * 100.0),
	sprintf("%.3f%%", NROW(orderStatus) / tx_total * 100.0),
	sprintf("%.3f%%", NROW(stockLevel) / tx_total * 100.0),
	sprintf("%.3f%%", NROW(delivery) / tx_total * 100.0),
	NA,
	sprintf("%.3f%%", NROW(newOrder) / runInfo$runMins /
			  runInfo$runWarehouses / 0.1286),
	NA)
tx_90th <- c(
	sprintf("%.3fs", quantile(newOrder$latency, probs=0.90) / 1000.0),
	sprintf("%.3fs", quantile(payment$latency, probs=0.90) / 1000.0),
	sprintf("%.3fs", quantile(orderStatus$latency, probs=0.90) / 1000.0),
	sprintf("%.3fs", quantile(stockLevel$latency, probs=0.90) / 1000.0),
	sprintf("%.3fs", quantile(delivery$latency, probs=0.90) / 1000.0),
	sprintf("%.3fs", quantile(deliveryBG$latency, probs=0.90) / 1000.0),
	NA, NA)
tx_max <- c(
	sprintf("%.3fs", max(newOrder$latency) / 1000.0),
	sprintf("%.3fs", max(payment$latency) / 1000.0),
	sprintf("%.3fs", max(orderStatus$latency) / 1000.0),
	sprintf("%.3fs", max(stockLevel$latency) / 1000.0),
	sprintf("%.3fs", max(delivery$latency) / 1000.0),
	sprintf("%.3fs", max(deliveryBG$latency) / 1000.0),
	NA, NA)
tx_limit <- c("5.0", "5.0", "5.0", "20.0", "5.0", "80.0", NA, NA)
tx_rbk <- c(
	sprintf("%.3f%%", sum(newOrder$rbk) / NROW(newOrder) * 100.0),
	NA, NA, NA, NA, NA, NA, NA)
tx_error <- c(
	sum(newOrder$error),
	sum(payment$error),
	sum(orderStatus$error),
	sum(stockLevel$error),
	sum(delivery$error),
	sum(deliveryBG$error),
	NA, NA)
tx_dskipped <- c(
	NA, NA, NA, NA, NA,
	sum(deliveryBG$dskipped),
	NA, NA)
tx_info <- data.frame(
	tx_name,
	tx_count,
	tx_percent,
	tx_90th,
	tx_max,
	tx_limit,
	tx_rbk,
	tx_error,
	tx_dskipped)

write.csv(tx_info, file = "data/tx_summary.csv", quote = FALSE, na = "N/A",
	row.names = FALSE)

