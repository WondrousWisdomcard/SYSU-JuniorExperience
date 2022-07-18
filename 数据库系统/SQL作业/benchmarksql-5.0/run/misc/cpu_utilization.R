# ----
# R graph to show CPU utilization
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
aggUser <- setNames(aggregate(rawData$cpu_user,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'cpu_user'))
aggSystem <- setNames(aggregate(rawData$cpu_system,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'cpu_system'))
aggWait <- setNames(aggregate(rawData$cpu_iowait,
			      list(elapsed=trunc(rawData$elapsed / idiv) * idiv), mean),
		    c('elapsed', 'cpu_wait'))

# ----
# ymax is 100%
# ----
ymax = 100


# ----
# Start the output image.
# ----
png("cpu_utilization.png", width=@WIDTH@, height=@HEIGHT@)
par(mar=c(4,4,4,4), xaxp=c(10,200,19))

# ----
# Plot USER+SYSTEM+WAIT
# ----
plot (
	aggUser$elapsed / 60000.0, (aggUser$cpu_user + aggSystem$cpu_system + aggWait$cpu_wait) * 100.0,
	type='l', col="red3", lwd=2,
	axes=TRUE,
	xlab="Elapsed Minutes",
	ylab="CPU Utilization in Percent",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the USER+SYSTEM
# ----
par (new=T)
plot (
	aggUser$elapsed / 60000.0, (aggUser$cpu_user + aggSystem$cpu_system) * 100.0,
	type='l', col="cyan3", lwd=2,
	axes=FALSE,
	xlab="",
	ylab="",
	xlim=c(0, xmax),
	ylim=c(0, ymax)
)

# ----
# Plot the USER
# ----
par (new=T)
plot (
	aggUser$elapsed / 60000.0, aggUser$cpu_user * 100.0,
	type='l', col="blue3", lwd=2,
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
	c("% User", "% System", "% IOWait"),
	fill=c("blue3", "cyan3", "red3"))
title (main=c(
    paste0("Run #", runInfo$run, " of BenchmarkSQL v", runInfo$driverVersion),
    "CPU Utilization"
    ))
grid()
box()
