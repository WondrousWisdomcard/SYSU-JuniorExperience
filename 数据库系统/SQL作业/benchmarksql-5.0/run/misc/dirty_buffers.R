# ----
# R graph to show number of dirty kernel buffers
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
# Read the recorded CPU data and aggregate it for the desired interval.
# ----
rawData <- read.csv("data/sys_info.csv", head=TRUE)
aggDirty <- setNames(aggregate(rawData$vm_nr_dirty,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'vm_nr_dirty'))

# ----
# Determine ymax
# ----
ymax_dirty = max(aggDirty$vm_nr_dirty)
sqrt2 <- sqrt(2.0)
ymax <- 1
while (ymax < ymax_dirty) {
    ymax <- ymax * sqrt2
}
if (ymax < (ymax_dirty * 1.2)) {
    ymax <- ymax * 1.2
}


# ----
# Start the output image.
# ----
png("dirty_buffers.png", width=@WIDTH@, height=@HEIGHT@)
par(mar=c(4,4,4,4), xaxp=c(10,200,19))

# ----
# Plot dirty buffers
# ----
plot (
	aggDirty$elapsed / 60000.0, aggDirty$vm_nr_dirty,
	type='l', col="red3", lwd=2,
	axes=TRUE,
	xlab="Elapsed Minutes",
	ylab="Number dirty kernel buffers",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Add legend, title and other decorations.
# ----
legend ("topleft",
	c("vmstat nr_dirty"),
	fill=c("red3"))
title (main=c(
    paste0("Run #", runInfo$run, " of BenchmarkSQL v", runInfo$driverVersion),
    "Dirty Kernel Buffers"
    ))
grid()
box()
