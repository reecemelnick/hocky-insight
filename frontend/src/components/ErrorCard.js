function ErrorCard( {error} ) {
  return (
    <div className="rounded-3xl border border-rose-500/30 bg-rose-500/10 p-6 text-rose-100 shadow-xl shadow-rose-950/20">
        {error}
    </div>
  )
}

export default ErrorCard;