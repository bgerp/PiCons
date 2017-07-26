
# Start the PiCons server.
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  echo "The PiCons server is runing."
else
  echo "Starting the PiCons server."
  sudo python ~/PiCons/main.py > /dev/null 2>&1 &
fi
