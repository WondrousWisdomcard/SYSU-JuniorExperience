# ----
# R graph to show IOPS of a block device.
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
# Read the recorded IO data for the block devide
# and aggregate it for the desired interval.
# ----
rawData <- read.csv("data/@DEVICE@.csv", head=TRUE)
aggReads <- setNames(aggregate(rawData$rdiops,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'rdiops'))
aggWrites <- setNames(aggregate(rawData$wriops,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'wriops'))
rawData
aggReads
aggWrites

# ----
# Determine the ymax by increasing in sqrt(2) steps until the
# maximum of both IOPS fits. The multiply that with 1.2 to
# give a little head room for the legend.
# ----
ymax_rd <- max(aggReads$rdiops)
ymax_wr <- max(aggWrites$wriops)
ymax <- 1
sqrt2 <- sqrt(2.0)
while (ymax < ymax_rd || ymax < ymax_wr) {
    ymax <- ymax * sqrt2
}
if (ymax < (ymax_rd * 1.2) || ymax < (ymax_wr * 1.2)) {
    ymax <- ymax * 1.2
}



# ----
# Start the output image.
# ----
png("@DEVICE@_iops.png", width=@WIDTH@, height=@HEIGHT@)
par(mar=c(4,4,4,4), xaxp=c(10,200,19))

# ----
# Plot the RDIOPS
# ----
plot (
	aggReads$elapsed / 60000.0, aggReads$rdiops,
	type='l', col="blue3", lwd=2,
	axes=TRUE,
	xlab="Elapsed Minutes",
	ylab="IO Operations per Second",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the WRIOPS
# ----
par (new=T)
plot (
	aggWrites$elapsed / 60000.0, aggWrites$wriops,
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
	c("Read Operations on @DEVICE@", "Write Operations on @DEVICE@"),
	fill=c("blue3", "red3"))
title (main=c(
    paste0("Run #", runInfo$run, " of BenchmarkSQL v", runInfo$driverVersion),
    "Block Device @DEVICE@ IOPS"
    ))
grid()
box()
