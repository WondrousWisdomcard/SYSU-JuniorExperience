# ----
# R graph to show Packets of a network device.
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
# Read the recorded IO data for the network devide
# and aggregate it for the desired interval.
# ----
rawData <- read.csv("data/@DEVICE@.csv", head=TRUE)
aggRecv <- setNames(aggregate(rawData$rxpktsps,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'rxpktsps'))
aggSend <- setNames(aggregate(rawData$txpktsps,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'txpktsps'))

# ----
# Determine the ymax by increasing in sqrt(2) steps until the
# maximum of both IOPS fits. The multiply that with 1.2 to
# give a little head room for the legend.
# ----
ymax_rx <- max(aggRecv$rxpktsps)
ymax_tx <- max(aggSend$txpktsps)
ymax <- 1
sqrt2 <- sqrt(2.0)
while (ymax < ymax_rx || ymax < ymax_tx) {
    ymax <- ymax * sqrt2
}
if (ymax < (ymax_rx * 1.2) || ymax < (ymax_tx * 1.2)) {
    ymax <- ymax * 1.2
}



# ----
# Start the output image.
# ----
png("@DEVICE@_iops.png", width=@WIDTH@, height=@HEIGHT@)
par(mar=c(4,4,4,4), xaxp=c(10,200,19))

# ----
# Plot the RXPKTSPS
# ----
plot (
	aggRecv$elapsed / 60000.0, aggRecv$rxpktsps,
	type='l', col="blue3", lwd=2,
	axes=TRUE,
	xlab="Elapsed Minutes",
	ylab="Packets per Second",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the TXPKTSPS
# ----
par (new=T)
plot (
	aggSend$elapsed / 60000.0, aggSend$txpktsps,
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
	c("RX Packets/s on @DEVICE@", "TX Packets/s on @DEVICE@"),
	fill=c("blue3", "red3"))
title (main=c(
    paste0("Run #", runInfo$run, " of BenchmarkSQL v", runInfo$driverVersion),
    "Network Device @DEVICE@ Packets per Second"
    ))
grid()
box()
